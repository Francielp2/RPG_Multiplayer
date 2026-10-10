from contextlib import nullcontext
import io
import os
from pathlib import Path
import select
import subprocess
import sys
import unittest
from unittest.mock import MagicMock, patch

from interface.teclado import ler_opcao, _ler_tecla
import interface.teclado as teclado


class TestTeclado(unittest.TestCase):
    def simular(self, teclas):
        entrada = MagicMock()
        entrada.isatty.return_value = True
        saida = io.StringIO()
        saida.isatty = lambda: True
        with patch.object(teclado.sys, "stdin", entrada), \
                patch.object(teclado.sys, "stdout", saida), \
                patch.object(teclado, "_modo_teclado", return_value=nullcontext()), \
                patch.object(teclado, "_ler_tecla", side_effect=teclas):
            resultado = ler_opcao("Sua opção:")
        return resultado, saida.getvalue()

    def test_opcao_so_confirmada_com_enter(self):
        resultado, tela = self.simular(["2", "\r"])
        self.assertEqual(resultado, "2")
        self.assertEqual(tela, "Sua opção:2\n")
        self.assertIsNone(self.simular(["2", "\x1b"])[0])

    def test_esc_cancela_entrada_parcial(self):
        resultado, _ = self.simular(["1", "2", "\x1b"])
        self.assertIsNone(resultado)

    def test_indices_longos_voltar_e_backspace(self):
        for teclas, esperado in ((["1", "2", "\r"], "12"),
                                  (["-", "1", "\r"], "-1"),
                                  (["1", "2", "\x7f", "3", "\n"], "13")):
            self.assertEqual(self.simular(teclas)[0], esperado)

    def test_interrupcao(self):
        with self.assertRaises(KeyboardInterrupt):
            self.simular(["\x03"])

    def test_entrada_redirecionada_preserva_input(self):
        with patch.object(teclado.sys.stdin, "isatty", return_value=False), \
                patch("builtins.input", return_value="12") as entrada:
            self.assertEqual(ler_opcao("Sua opção:"), "12")
            entrada.assert_called_once_with("Sua opção:")

    def test_leitura_windows_e_ignorando_setas(self):
        teclado = MagicMock()
        teclado.getwch.side_effect = ["\xe0", "H", "\x1b", "2"]
        with patch.object(os, "name", "nt"), patch.dict(sys.modules, {"msvcrt": teclado}):
            self.assertEqual(_ler_tecla(), "")
            self.assertEqual(_ler_tecla(), "\x1b")
            self.assertEqual(_ler_tecla(), "2")

    @unittest.skipIf(os.name == "nt", "Ensaio com pseudo-terminal Unix")
    def test_terminal_real_e_restauracao(self):
        import pty
        import termios

        for teclas, esperado in ((b"2\r", "'2'"),
                                 (b"2\x1b", "None"),
                                 (b"\x1b", "None"),
                                 (b"12\r", "'12'"),
                                 (b"\x1b[A", "None")):
            with self.subTest(teclas=teclas):
                mestre, escravo = pty.openpty()
                anterior = termios.tcgetattr(escravo)
                script = ("from interface.teclado import ler_opcao; "
                          "print('RESULTADO', repr(ler_opcao('PRONTO:')))")
                processo = subprocess.Popen([sys.executable, "-c", script],
                                           cwd=Path(__file__).resolve().parents[1],
                                           stdin=escravo, stdout=escravo, stderr=escravo)
                try:
                    tela = b""
                    while b"PRONTO:" not in tela:
                        self.assertTrue(select.select([mestre], [], [], 3)[0])
                        tela += os.read(mestre, 4096)
                    os.write(mestre, teclas)
                    if teclas == b"\x1b[A":
                        # Uma seta não deve cancelar. Esc isolado cancela depois.
                        self.assertFalse(select.select([mestre], [], [], .1)[0])
                        os.write(mestre, b"\x1b")
                    processo.wait(timeout=3)
                    while select.select([mestre], [], [], .05)[0]:
                        tela += os.read(mestre, 4096)
                    self.assertEqual(processo.returncode, 0, tela.decode())
                    self.assertIn(f"RESULTADO {esperado}".encode(), tela)
                    self.assertEqual(termios.tcgetattr(escravo), anterior)
                finally:
                    if processo.poll() is None:
                        processo.kill()
                        processo.wait()
                    os.close(mestre)
                    os.close(escravo)


if __name__ == "__main__":
    unittest.main()
