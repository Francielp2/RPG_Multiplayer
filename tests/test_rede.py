"""Transporte e partidas reais via TCP, sem dispositivo de áudio."""

import json
import os
from pathlib import Path
import re
import select
import socket
import subprocess
import sys
import threading
from time import monotonic
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from rede.protocolo import CanalJSON, ErroProtocolo, MAX_MENSAGEM
from rede.terminal_remoto import TerminalRemoto


RAIZ = Path(__file__).resolve().parents[1]


class TestProtocolo(unittest.TestCase):
    def par(self):
        a, b = socket.socketpair()
        self.addCleanup(a.close)
        self.addCleanup(b.close)
        a.settimeout(2)
        b.settimeout(2)
        return a, CanalJSON(b)

    def test_fragmentos_utf8_e_varias_linhas(self):
        a, canal = self.par()
        dados = json.dumps({"tipo": "texto", "texto": "🧪 ação"}, ensure_ascii=False).encode() + b"\n"
        a.sendall(dados[:31])
        canal.socket.settimeout(.02)
        with self.assertRaises(socket.timeout):
            canal.receber()
        canal.socket.settimeout(2)
        a.sendall(dados[31:] + b'{"tipo":"fim"}\n')
        self.assertEqual(canal.receber()["texto"], "🧪 ação")
        self.assertEqual(canal.receber(), {"tipo": "fim"})

    def test_json_invalido_tipo_ausente_e_tamanho(self):
        for dados in (b'{\n', b'[]\n', b'{"tipo":3}\n', b'\xff\n', b'x' * (MAX_MENSAGEM + 1) + b'\n'):
            with self.subTest(dados=dados[:20]):
                a, canal = self.par()
                a.sendall(dados)
                with self.assertRaises(ErroProtocolo):
                    canal.receber()

    def test_envio_concorrente_preserva_linhas(self):
        a, canal = self.par()
        emissor = CanalJSON(a)
        threads = [threading.Thread(target=emissor.enviar, args=({"tipo": "numero", "n": n},)) for n in range(20)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual({canal.receber()["n"] for _ in threads}, set(range(20)))

    def test_conexao_encerrada(self):
        a, canal = self.par()
        a.close()
        with self.assertRaises(ConnectionError):
            canal.receber()


class TestPartidaTCP(unittest.TestCase):
    def servidor(self, jogadores=2, timeout=5, hp=1):
        processo = subprocess.Popen(
            [sys.executable, "-u", "servidor.py", "--host", "127.0.0.1", "--port", "0",
             "--jogadores", str(jogadores), "--timeout", str(timeout), "--hp", str(hp), "--sem-pausas"],
            cwd=RAIZ, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(self.fechar_processo, processo)
        # Windows não oferece select() para pipes; readline termina na primeira linha.
        if os.name != "nt":
            self.assertTrue(select.select([processo.stdout], [], [], 5)[0], "Servidor não iniciou")
        linha = processo.stdout.readline()
        match = re.search(r"127\.0\.0\.1:(\d+)", linha)
        self.assertIsNotNone(match, linha + (processo.stderr.read() if processo.poll() is not None else ""))
        return processo, int(match.group(1))

    @staticmethod
    def fechar_processo(processo):
        if processo.poll() is None:
            processo.kill()
        processo.communicate(timeout=5)

    def conectar(self, porta, nome):
        sock = socket.create_connection(("127.0.0.1", porta), timeout=5)
        sock.settimeout(5)
        canal = CanalJSON(sock)
        self.addCleanup(canal.fechar)
        canal.enviar({"tipo": "entrar", "nome": nome, "largura": 100})
        self.assertEqual(canal.receber()["tipo"], "bem_vindo")
        return canal

    def ate(self, canal, tipo):
        mensagens = []
        for _ in range(300):
            mensagem = canal.receber()
            mensagens.append(mensagem)
            if mensagem["tipo"] == tipo:
                return mensagens
        self.fail(f"Não recebeu {tipo}")

    @staticmethod
    def responder(canal, pedido, valor):
        canal.enviar({"tipo": "resposta", "pedido_id": pedido["pedido_id"], "valor": valor})

    def test_partida_completa_telas_iguais_rejeicao_e_inventario_privado(self):
        processo, porta = self.servidor(hp=10)
        a, b = self.conectar(porta, "Ana"), self.conectar(porta, "Bruno")
        ma = self.ate(a, "solicitar_entrada")
        mb = self.ate(b, "solicitar_entrada")
        self.assertEqual([m for m in ma if m["tipo"] in ("tela", "estado", "som")],
                         [m for m in mb if m["tipo"] in ("tela", "estado", "som")])
        pedido = ma[-1]
        self.assertTrue(pedido["responder"])
        self.assertFalse(mb[-1]["responder"])
        self.responder(b, pedido, "1")
        self.assertIn("recusada", b.receber()["texto"])
        # Atribuições de HP enviadas pelo cliente também são recusadas.
        a.enviar({"tipo": "resposta", "pedido_id": pedido["pedido_id"], "valor": "1", "hp": 999})
        self.assertEqual(a.receber()["tipo"], "erro")
        self.responder(a, pedido, "3")
        privado = self.ate(a, "solicitar_entrada")
        self.assertNotEqual(privado[-1]["pedido_id"], pedido["pedido_id"])
        # Inventário vazio retorna automaticamente ao menu: só o dono vê seu conteúdo.
        self.assertTrue(any("Inventário vazio" in m.get("conteudo", "") for m in privado))
        ma = privado
        mb = self.ate(b, "solicitar_entrada")
        self.assertFalse(any("Inventário vazio" in m.get("conteudo", "") for m in mb))
        # Visita à loja é pública; Esc não passa a vez.
        self.responder(a, ma[-1], "2")
        ma = self.ate(a, "solicitar_entrada")
        mb = self.ate(b, "solicitar_entrada")
        self.assertEqual([m for m in ma if m["tipo"] == "tela"], [m for m in mb if m["tipo"] == "tela"])
        self.responder(a, ma[-1], None)
        ma = self.ate(a, "solicitar_entrada")
        mb = self.ate(b, "solicitar_entrada")
        # Repetir uma solicitação já concluída não executa outra ação.
        self.responder(a, pedido, "1")
        self.assertEqual(a.receber()["tipo"], "erro")
        for _ in range(200):
            pedido = ma[-1]
            dono = a if pedido["jogador_id"] == "j001" else b
            self.responder(dono, pedido, "0" if "apostar" in pedido["texto"] else "1")
            ma, mb = [], []
            for canal, mensagens in ((a, ma), (b, mb)):
                while True:
                    mensagem = canal.receber()
                    mensagens.append(mensagem)
                    if mensagem["tipo"] in ("solicitar_entrada", "fim_partida"):
                        break
            self.assertEqual([m for m in ma if m["tipo"] in ("tela", "estado", "som")],
                             [m for m in mb if m["tipo"] in ("tela", "estado", "som")])
            if ma[-1]["tipo"] == "fim_partida":
                self.assertFalse(ma[-1]["cancelada"])
                self.assertEqual(ma[-1], mb[-1])
                self.assertIn(ma[-1]["vencedor_id"], ("j001", "j002", None))
                break
        else:
            self.fail("Partida não terminou")
        processo.wait(timeout=5)
        self.assertEqual(processo.returncode, 0, processo.stderr.read())

    def test_desconexao_enquanto_aguarda_entrada(self):
        processo, porta = self.servidor()
        a, b = self.conectar(porta, "Ana"), self.conectar(porta, "Bruno")
        self.ate(a, "solicitar_entrada")
        self.ate(b, "solicitar_entrada")
        b.fechar()
        fim = self.ate(a, "fim_partida")[-1]
        self.assertTrue(fim["cancelada"])
        self.assertIn("Bruno", fim["texto"])
        processo.wait(timeout=5)

    def test_timeout_resposta(self):
        processo, porta = self.servidor(timeout=1)
        a, b = self.conectar(porta, "Ana"), self.conectar(porta, "Bruno")
        self.ate(a, "solicitar_entrada")
        self.ate(b, "solicitar_entrada")
        self.assertIn("Tempo", self.ate(a, "fim_partida")[-1]["texto"])
        self.assertTrue(self.ate(b, "fim_partida")[-1]["cancelada"])
        processo.wait(timeout=5)

    def test_executaveis_cliente_com_servidor_real(self):
        processo, porta = self.servidor(hp=1)
        clientes = []
        for nome in ("Ana", "Bruno"):
            cliente = subprocess.Popen(
                [sys.executable, "cliente.py", "--host", "127.0.0.1", "--port", str(porta), "--nome", nome],
                cwd=RAIZ, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.addCleanup(self.fechar_processo, cliente)
            cliente.stdin.write("1\n0\n" * 100)
            cliente.stdin.close()
            cliente.stdin = None
            clientes.append(cliente)
        for cliente in clientes:
            saida, erro = cliente.communicate(timeout=10)
            self.assertEqual(cliente.returncode, 0, erro)
            self.assertIn("Venceu a partida", saida)
            self.assertIn("Partida encerrada", saida)
        processo.wait(timeout=5)

    def test_tres_jogadores_ids_e_turnos_apos_eliminacao(self):
        processo, porta = self.servidor(jogadores=3, hp=1)
        canais = [self.conectar(porta, nome) for nome in ("Ana", "Bruno", "Caio")]
        mensagens = [self.ate(canal, "solicitar_entrada") for canal in canais]
        jogadores = None
        houve_eliminacao = False
        for _ in range(300):
            for mensagem in mensagens[0]:
                if mensagem["tipo"] == "estado":
                    jogadores = mensagem["jogadores"]
                    self.assertIn(mensagem["atual_id"], [jog["id"] for jog in jogadores])
                    houve_eliminacao |= len(jogadores) < 3
            pedido = mensagens[0][-1]
            if pedido["tipo"] == "fim_partida":
                self.assertFalse(pedido["cancelada"])
                self.assertTrue(houve_eliminacao)
                self.assertTrue(all(lista[-1] == pedido for lista in mensagens))
                break
            dono = canais[int(pedido["jogador_id"][1:]) - 1]
            if "quem você vai atacar" in pedido["texto"]:
                valor = str(next(i for i, jog in enumerate(jogadores) if jog["id"] != pedido["jogador_id"]))
            else:
                valor = "0" if "apostar" in pedido["texto"] else "1"
            self.responder(dono, pedido, valor)
            mensagens = []
            for canal in canais:
                lista = []
                while True:
                    mensagem = canal.receber()
                    lista.append(mensagem)
                    if mensagem["tipo"] in ("solicitar_entrada", "fim_partida"):
                        break
                mensagens.append(lista)
            telas = [[m for m in lista if m["tipo"] in ("tela", "estado", "som")] for lista in mensagens]
            self.assertEqual(telas[0], telas[1])
            self.assertEqual(telas[0], telas[2])
        else:
            self.fail("Partida não terminou")
        processo.wait(timeout=5)
        self.assertEqual(processo.returncode, 0, processo.stderr.read())

    @unittest.skipIf(os.name == "nt", "Pseudo-terminal Unix")
    def test_cliente_tty_restaura_teclado_apos_desconexao(self):
        import pty
        import termios

        processo, porta = self.servidor(hp=100)
        mestre, escravo = pty.openpty()
        self.addCleanup(os.close, mestre)
        self.addCleanup(os.close, escravo)
        anterior = termios.tcgetattr(escravo)
        cliente = subprocess.Popen(
            [sys.executable, "cliente.py", "--host", "127.0.0.1", "--port", str(porta), "--nome", "Ana"],
            cwd=RAIZ, stdin=escravo, stdout=escravo, stderr=subprocess.PIPE)
        self.addCleanup(self.fechar_processo, cliente)
        conteudo = b""
        limite = monotonic() + 5
        while b"Aguardando a sala" not in conteudo and monotonic() < limite:
            if select.select([mestre], [], [], .1)[0]:
                conteudo += os.read(mestre, 65536)
        self.assertIn(b"Aguardando a sala", conteudo)
        outro = self.conectar(porta, "Bruno")
        self.ate(outro, "solicitar_entrada")
        while "Sua opção:".encode() not in conteudo and monotonic() < limite:
            if select.select([mestre], [], [], .1)[0]:
                conteudo += os.read(mestre, 65536)
        self.assertIn("Sua opção:".encode(), conteudo)
        self.assertFalse(termios.tcgetattr(escravo)[3] & termios.ICANON)
        outro.fechar()
        cliente.wait(timeout=5)
        self.assertEqual(cliente.returncode, 0, cliente.stderr.read())
        self.assertEqual(termios.tcgetattr(escravo), anterior)
        processo.wait(timeout=5)


class TestAdaptadorRemoto(unittest.TestCase):
    def test_escopo_privado_e_evento_de_outro_jogador(self):
        servidor = MagicMock()
        terminal = TerminalRemoto(servidor, 100)
        ana, bruno = SimpleNamespace(id="j001"), SimpleNamespace(id="j002")
        terminal.atual = ana
        terminal.perguntar("quanto deseja apostar?", jogador=bruno)
        servidor.perguntar.assert_called_with("j002", "quanto deseja apostar?", False, privado=False)
        with terminal.privado(ana):
            terminal.mostrar("Item secreto")
            self.assertEqual(servidor.enviar.call_args.args[1], "j001")
            terminal.perguntar("Escolha um item", cancelavel=True)
            servidor.perguntar.assert_called_with("j001", "Escolha um item", True, privado=True)
            terminal.anunciar("Ana usou uma poção")
            self.assertEqual(len(servidor.enviar.call_args.args), 1)
        terminal.mostrar("Público")
        self.assertIsNone(servidor.enviar.call_args.args[1])


if __name__ == "__main__":
    unittest.main()
