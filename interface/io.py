"""Entrada e saída substituíveis: terminal local ou sessão de rede.

Novas funcionalidades devem usar este módulo para perguntar, mostrar e pausar.
As regras do jogo continuam nos módulos originais.
"""

import builtins
from contextlib import contextmanager
from contextvars import ContextVar
import os
import time

from rich import print as rich_print


_terminal = ContextVar("terminal_rpg", default=None)


def terminal_atual():
    return _terminal.get()


@contextmanager
def usar_terminal(terminal):
    token = _terminal.set(terminal)
    try:
        yield
    finally:
        _terminal.reset(token)


def print(*objetos, **opcoes):
    terminal = terminal_atual()
    if terminal is None:
        return rich_print(*objetos, **opcoes)
    return terminal.mostrar(*objetos, **opcoes)


def perguntar(mensagem=">", jogador=None, cancelavel=False):
    terminal = terminal_atual()
    if terminal is not None:
        return terminal.perguntar(mensagem, jogador, cancelavel)
    return builtins.input(mensagem)


def limpar():
    terminal = terminal_atual()
    if terminal is None:
        os.system("cls" if os.name == "nt" else "clear")
    else:
        terminal.limpar()


def pausa(segundos):
    terminal = terminal_atual()
    if terminal is None:
        time.sleep(segundos)
    else:
        terminal.pausa(segundos)


def atualizar_estado(jogadores, atual, turno, rodada):
    terminal = terminal_atual()
    if terminal is not None:
        terminal.atualizar_estado(jogadores, atual, turno, rodada)


def anunciar(texto):
    terminal = terminal_atual()
    if terminal is not None:
        terminal.anunciar(texto)


@contextmanager
def privado(jogador):
    terminal = terminal_atual()
    if terminal is None:
        yield
    else:
        with terminal.privado(jogador):
            yield
