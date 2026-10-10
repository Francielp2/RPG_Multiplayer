import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

from audio import ARQUIVOS_SOM, PASTA_SONS
from rede.audio_cliente import AudioCliente
from rede.terminal_remoto import TerminalRemoto


class TestAudioRede(unittest.TestCase):
    def audio(self):
        with patch.dict(os.environ, {"RPG_SEM_SOM": "0"}):
            audio = AudioCliente(avisar=MagicMock())
        audio.pygame = MagicMock()
        audio.pygame.error = RuntimeError
        return audio

    def test_reproduzir_parar_volume_e_cache(self):
        audio = self.audio()
        audio.executar({"nome": "dano_soco", "acao": "play", "volume": .8})
        efeito = audio.pygame.mixer.Sound.return_value
        efeito.set_volume.assert_called_with(.8)
        efeito.play.assert_called_once()
        audio.executar({"nome": "dano_soco", "acao": "play", "volume": .8})
        audio.pygame.mixer.Sound.assert_called_once_with(str(PASTA_SONS / ARQUIVOS_SOM["dano_soco"]))
        audio.executar({"nome": "dano_soco", "acao": "stop"})
        efeito.stop.assert_called_once()
        audio.fechar()
        audio.pygame.mixer.quit.assert_called_once()

    def test_catalogo_e_dados_invalidos(self):
        audio = self.audio()
        for mensagem in ({"nome": "../../outro", "acao": "play"}, {"nome": [], "acao": "play"},
                         {"nome": "bonk", "acao": "apagar"}, {"nome": "bonk", "acao": "play", "volume": 2},
                         {"nome": "bonk", "acao": "play", "volume": "1"}):
            audio.executar(mensagem)
        audio.pygame.mixer.Sound.assert_not_called()
        self.assertTrue(all((PASTA_SONS / arquivo).is_file() for arquivo in ARQUIVOS_SOM.values()))

    def test_arquivo_ausente_nao_interrompe_partida(self):
        audio = self.audio()
        audio.pygame.mixer.Sound.side_effect = FileNotFoundError("arquivo ausente")
        for _ in range(2):
            audio.executar({"nome": "bonk", "acao": "play"})
        audio.avisar.assert_called_once()
        audio.pygame.mixer.Sound.assert_called_once()

    def test_sem_dispositivo_avisa_uma_vez(self):
        with patch.dict(os.environ, {"RPG_SEM_SOM": "0"}):
            audio = AudioCliente(avisar=MagicMock())
        pygame = MagicMock()
        pygame.mixer.init.side_effect = RuntimeError("sem dispositivo")
        with patch.dict(sys.modules, {"pygame": pygame}):
            audio.executar({"nome": "bonk", "acao": "play"})
            audio.executar({"nome": "bonk", "acao": "play"})
        audio.avisar.assert_called_once()
        self.assertFalse(audio.habilitado)

    def test_desativado_nao_abre_audio(self):
        audio = AudioCliente(habilitado=False)
        pygame = MagicMock()
        with patch.dict(sys.modules, {"pygame": pygame}):
            audio.executar({"nome": "bonk", "acao": "play"})
        pygame.mixer.init.assert_not_called()

    def test_encaminhamento_publico_e_privado(self):
        servidor = MagicMock()
        terminal = TerminalRemoto(servidor, 100)
        terminal.som("atacar", "play", 1.0)
        servidor.enviar.assert_called_with({"tipo": "som", "nome": "atacar", "acao": "play", "volume": 1.0}, None)
        with terminal.privado(SimpleNamespace(id="j001")):
            terminal.som("inventario", "play", 1.0)
            self.assertEqual(servidor.enviar.call_args.args[1], "j001")

    def test_servidor_emite_sons_sem_importar_pygame(self):
        # Processo isolado evita o mock de som usado pelos testes de poções.
        codigo = '''
import os, sys
os.environ['RPG_SEM_SOM'] = '1'
import som
from interface.io import usar_terminal
from unittest.mock import MagicMock
terminal = MagicMock()
with usar_terminal(terminal):
    som.dano_soco.play()
    som.dano_soco.stop()
assert 'pygame' not in sys.modules
assert terminal.som.call_args_list[0].args == ('dano_soco', 'play', .8)
assert terminal.som.call_args_list[1].args == ('dano_soco', 'stop', .8)
'''
        resultado = subprocess.run([sys.executable, "-c", codigo], cwd=Path(__file__).resolve().parents[1],
                                   capture_output=True, text=True, timeout=5)
        self.assertEqual(resultado.returncode, 0, resultado.stderr)


if __name__ == "__main__":
    unittest.main()
