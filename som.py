from pathlib import Path

import os
from random import random,randint

PASTA_SONS = Path(__file__).resolve().parent / "sound"

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


def carregar_som(caminho):
    if SEM_SOM:
        return SomSilencioso()
    return pygame.mixer.Sound(caminho)

bonk = carregar_som(str(PASTA_SONS / "Bonk.wav"))
dano_soco =carregar_som(str(PASTA_SONS / "soco.wav"))
dano_soco.set_volume(0.8)
dano_soco2=carregar_som(str(PASTA_SONS / "soco2.wav"))
dano_espada=carregar_som(str(PASTA_SONS / "golpeespada1.ogg"))
moedas =carregar_som(str(PASTA_SONS / "moedas.mp3"))
dano_espada_forte =carregar_som(str(PASTA_SONS / "golpeespada2.mp3"))
novo_slot = carregar_som(str(PASTA_SONS / "novo slot.MP3"))
quebra_armadura =carregar_som(str(PASTA_SONS / "quebrar_armadura.mp3"))
evento =carregar_som(str(PASTA_SONS / "evento_aleatorio.wav"))
raio =carregar_som(str(PASTA_SONS / "raio.wav"))
raio.set_volume(0.7)
roubado =carregar_som(str(PASTA_SONS / "roubado.wav"))
esquiva =carregar_som(str(PASTA_SONS / "esquiva.wav"))
attloja =carregar_som(str(PASTA_SONS / "att_loja.mp3"))
compra = carregar_som(str(PASTA_SONS / "compra.MP3"))
equipar = carregar_som(str(PASTA_SONS / "equipar.mp3"))
inventario =carregar_som(str(PASTA_SONS / "inventario.MP3"))
fail = carregar_som(str(PASTA_SONS / "fail.mp3"))
fail2 =carregar_som(str(PASTA_SONS / "bobsad.wav"))
mine_dano =carregar_som(str(PASTA_SONS / "minecraft damage.wav"))
atacar =carregar_som(str(PASTA_SONS / "atacar.MP3"))
grave2=carregar_som(str(PASTA_SONS / "grave2.MP3"))
golpe_armadura=carregar_som(str(PASTA_SONS / "armadura ataque1.MP3"))
golpe_armadura2 =carregar_som(str(PASTA_SONS / "armadura ataque2.MP3"))
dado=carregar_som(str(PASTA_SONS / "dado.mp3"))
comer =carregar_som(str(PASTA_SONS / "mine comendo.mp3"))
pocaomine=carregar_som(str(PASTA_SONS / "pocaomine.MP3"))
xpmine=carregar_som(str(PASTA_SONS / "xpmine.wav"))
cassino=carregar_som(str(PASTA_SONS / "cassino.MP3"))
cassino.set_volume(0.7)
roletando=carregar_som(str(PASTA_SONS / "roletando.wav"))
morte1=carregar_som(str(PASTA_SONS / "morte1.MP3"))
morte2=carregar_som(str(PASTA_SONS / "morte2.MP3"))
morte3 = carregar_som(str(PASTA_SONS / "morte3.mp3"))
morte4 = carregar_som(str(PASTA_SONS / "morte4.mp3"))
todos_morte=carregar_som(str(PASTA_SONS / "todo mundo morreu.mp3"))
especial=carregar_som(str(PASTA_SONS / "especial.mp3"))
fogocj=carregar_som(str(PASTA_SONS / "cj pegando fogo.mp3"))
vitoria =carregar_som(str(PASTA_SONS / "vitoria.ogg"))
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




