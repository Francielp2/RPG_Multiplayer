"""Reprodução local opcional, sem regras nem sorteios do jogo."""

import os

from audio import ARQUIVOS_SOM, PASTA_SONS, VOLUMES


class AudioCliente:
    def __init__(self, habilitado=True, avisar=print):
        self.habilitado = habilitado and os.environ.get("RPG_SEM_SOM") != "1"
        self.avisar = avisar
        self.pygame = None
        self.efeitos = {}
        self.indisponiveis = set()

    def executar(self, mensagem):
        nome, acao = mensagem.get("nome"), mensagem.get("acao")
        if (not self.habilitado or not isinstance(nome, str) or nome not in ARQUIVOS_SOM
                or acao not in ("play", "stop") or nome in self.indisponiveis):
            return
        volume = mensagem.get("volume", VOLUMES.get(nome, 1.0))
        if type(volume) not in (int, float) or not 0 <= volume <= 1:
            return
        if acao == "stop":
            if nome in self.efeitos:
                self.efeitos[nome].stop()
            return
        if self.pygame is None:
            try:
                os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
                import pygame
                pygame.mixer.init()
                self.pygame = pygame
            except Exception as erro:
                # A dependência ou o dispositivo podem estar indisponíveis.
                self.desativar(erro)
                return
        try:
            if nome not in self.efeitos:
                self.efeitos[nome] = self.pygame.mixer.Sound(str(PASTA_SONS / ARQUIVOS_SOM[nome]))
            efeito = self.efeitos[nome]
            efeito.set_volume(volume)
            efeito.play()
        except (OSError, self.pygame.error) as erro:
            self.indisponiveis.add(nome)
            self.avisar(f"Som {nome} indisponível: {erro}. A partida continua.")

    def desativar(self, erro):
        self.habilitado = False
        self.avisar(f"Áudio indisponível: {erro}. A partida continua sem som; instale pygame ou use --sem-som.")

    def fechar(self):
        if self.pygame is not None:
            self.pygame.mixer.quit()
