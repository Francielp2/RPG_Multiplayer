"""Catálogo compartilhado; importar este módulo não inicializa áudio."""

from pathlib import Path

PASTA_SONS = Path(__file__).resolve().parent / "sound"

ARQUIVOS_SOM = {
    'bonk': 'Bonk.wav',
    'dano_soco': 'soco.wav',
    'dano_soco2': 'soco2.wav',
    'dano_espada': 'golpeespada1.ogg',
    'moedas': 'moedas.mp3',
    'dano_espada_forte': 'golpeespada2.mp3',
    'novo_slot': 'novo slot.MP3',
    'quebra_armadura': 'quebrar_armadura.mp3',
    'evento': 'evento_aleatorio.wav',
    'raio': 'raio.wav',
    'roubado': 'roubado.wav',
    'esquiva': 'esquiva.wav',
    'attloja': 'att_loja.mp3',
    'compra': 'compra.MP3',
    'equipar': 'equipar.mp3',
    'inventario': 'inventario.MP3',
    'fail': 'fail.mp3',
    'fail2': 'bobsad.wav',
    'mine_dano': 'minecraft damage.wav',
    'atacar': 'atacar.MP3',
    'grave2': 'grave2.MP3',
    'golpe_armadura': 'armadura ataque1.MP3',
    'golpe_armadura2': 'armadura ataque2.MP3',
    'dado': 'dado.mp3',
    'comer': 'mine comendo.mp3',
    'pocaomine': 'pocaomine.MP3',
    'xpmine': 'xpmine.wav',
    'cassino': 'cassino.MP3',
    'roletando': 'roletando.wav',
    'morte1': 'morte1.MP3',
    'morte2': 'morte2.MP3',
    'morte3': 'morte3.mp3',
    'morte4': 'morte4.mp3',
    'todos_morte': 'todo mundo morreu.mp3',
    'especial': 'especial.mp3',
    'fogocj': 'cj pegando fogo.mp3',
    'vitoria': 'vitoria.ogg',
}

VOLUMES = {"dano_soco": 0.8, "raio": 0.7, "cassino": 0.7}
