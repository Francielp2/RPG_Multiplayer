from time import sleep

import pygame
from random import random,randint

pygame.mixer.init()

bonk = pygame.mixer.Sound("sound/Bonk.wav")
dano_soco =pygame.mixer.Sound("sound/soco.wav")
dano_soco.set_volume(0.8)
dano_soco2=pygame.mixer.Sound("sound/soco2.wav")
dano_espada=pygame.mixer.Sound("sound/golpeespada1.ogg")
moedas =pygame.mixer.Sound("sound/moedas.mp3")
dano_espada_forte =pygame.mixer.Sound("sound/golpeespada2.mp3")
novo_slot =pygame.mixer.Sound("sound/novo slot.mp3")
quebra_armadura =pygame.mixer.Sound("sound/quebrar_armadura.mp3")
evento =pygame.mixer.Sound("sound/evento_aleatorio.wav")
raio =pygame.mixer.Sound("sound/raio.wav")
raio.set_volume(0.7)
roubado =pygame.mixer.Sound("sound/roubado.wav")
esquiva =pygame.mixer.Sound("sound/esquiva.wav")
attloja =pygame.mixer.Sound("sound/att_loja.mp3")
compra =pygame.mixer.Sound("sound/compra.mp3")
equipar = pygame.mixer.Sound("sound/equipar.mp3")
inventario =pygame.mixer.Sound("sound/inventario.MP3")
fail = pygame.mixer.Sound("sound/fail.mp3")
fail2 =pygame.mixer.Sound("sound/bobsad.wav")
mine_dano =pygame.mixer.Sound("sound/minecraft damage.wav")
atacar =pygame.mixer.Sound("sound/atacar.MP3")
grave2=pygame.mixer.Sound("sound/grave2.MP3")
golpe_armadura=pygame.mixer.Sound("sound/armadura ataque1.MP3")
golpe_armadura2 =pygame.mixer.Sound("sound/armadura ataque2.MP3")
dado=pygame.mixer.Sound("sound/dado.mp3")
comer =pygame.mixer.Sound("sound/mine comendo.mp3")
pocaomine=pygame.mixer.Sound("sound/pocaomine.MP3")
xpmine=pygame.mixer.Sound("sound/xpmine.wav")
cassino=pygame.mixer.Sound("sound/cassino.MP3")
cassino.set_volume(0.7)
roletando=pygame.mixer.Sound("sound/roletando.wav")
morte1=pygame.mixer.Sound("sound/morte1.MP3")
morte2=pygame.mixer.Sound("sound/morte2.MP3")
morte3=pygame.mixer.Sound("sound/morte3.MP3")
morte4=pygame.mixer.Sound("sound/morte4.MP3")
todos_morte=pygame.mixer.Sound("sound/todo mundo morreu.mp3")
especial=pygame.mixer.Sound("sound/especial.mp3")
fogocj=pygame.mixer.Sound("sound/cj pegando fogo.mp3")
vitoria =pygame.mixer.Sound("sound/vitoria.ogg")
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




