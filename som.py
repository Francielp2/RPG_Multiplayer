from audio import ARQUIVOS_SOM, PASTA_SONS
from interface.io import terminal_atual

import os
from random import random,randint


class SomSilencioso:
    def play(self):
        pass

    def stop(self):
        pass

    def set_volume(self, volume):
        pass


SEM_SOM = os.environ.get("RPG_SEM_SOM") == "1"
if not SEM_SOM:
    import pygame
    pygame.mixer.init()


class EfeitoSonoro:
    """Encaminha o mesmo efeito para áudio local ou clientes autorizados."""

    def __init__(self, nome):
        self.nome = nome
        self.volume = 1.0
        self.local = SomSilencioso() if SEM_SOM else pygame.mixer.Sound(str(PASTA_SONS / ARQUIVOS_SOM[nome]))

    def play(self):
        terminal = terminal_atual()
        if terminal is not None:
            terminal.som(self.nome, "play", self.volume)
        else:
            return self.local.play()

    def stop(self):
        terminal = terminal_atual()
        if terminal is not None:
            terminal.som(self.nome, "stop", self.volume)
        else:
            self.local.stop()

    def set_volume(self, volume):
        self.volume = volume
        self.local.set_volume(volume)


def carregar_som(nome):
    return EfeitoSonoro(nome)

bonk = carregar_som('bonk')
dano_soco =carregar_som('dano_soco')
dano_soco.set_volume(0.8)
dano_soco2=carregar_som('dano_soco2')
dano_espada=carregar_som('dano_espada')
moedas =carregar_som('moedas')
dano_espada_forte =carregar_som('dano_espada_forte')
novo_slot = carregar_som('novo_slot')
quebra_armadura =carregar_som('quebra_armadura')
evento =carregar_som('evento')
raio =carregar_som('raio')
raio.set_volume(0.7)
roubado =carregar_som('roubado')
esquiva =carregar_som('esquiva')
attloja =carregar_som('attloja')
compra = carregar_som('compra')
equipar = carregar_som('equipar')
inventario =carregar_som('inventario')
fail = carregar_som('fail')
fail2 =carregar_som('fail2')
mine_dano =carregar_som('mine_dano')
atacar =carregar_som('atacar')
grave2=carregar_som('grave2')
golpe_armadura=carregar_som('golpe_armadura')
golpe_armadura2 =carregar_som('golpe_armadura2')
dado=carregar_som('dado')
comer =carregar_som('comer')
pocaomine=carregar_som('pocaomine')
xpmine=carregar_som('xpmine')
cassino=carregar_som('cassino')
cassino.set_volume(0.7)
roletando=carregar_som('roletando')
morte1=carregar_som('morte1')
morte2=carregar_som('morte2')
morte3 = carregar_som('morte3')
morte4 = carregar_som('morte4')
todos_morte=carregar_som('todos_morte')
especial=carregar_som('especial')
fogocj=carregar_som('fogocj')
vitoria =carregar_som('vitoria')
def mortesom() :
    variacao = randint(1,4)
    if variacao == 1 :
        morte1.play()
    elif variacao == 2 :
        morte2.play()
    elif variacao == 3:
        morte3.play()
    elif variacao == 4 :
        morte4.play()


def errou_ataque() :
    chance = random()
    if chance < 0.80 :
        esquiva.play()
    else:
        variacao = randint(0,1)
        if variacao == 0 :
            fail.play()
        elif variacao == 1:
            fail2.play()

def dano_som(dano) :
    if dano <= 2 :
        varicao = randint(0,1)
        if varicao == 0 : bonk.play()
        elif varicao == 1 : fail.play()

    elif dano <= 10 :
        variacao = randint(0,2)
        if variacao == 0 :
            dano_soco.play()
        elif variacao == 1 :
            dano_soco2.play()
        elif variacao ==2 :
            mine_dano.play()
    elif dano <= 15:
        dano_espada.play()

    elif dano <= 35 :
        dano_espada_forte.play()
    else :
        grave2.play()




