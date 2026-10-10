"""Entrada numérica com Esc para voltar, sem alterar as telas Rich."""

from contextlib import contextmanager
import os
import sys


@contextmanager
def _modo_teclado():
    if os.name == "nt":
        yield
        return
    import termios
    import tty

    arquivo = sys.stdin.fileno()
    anterior = termios.tcgetattr(arquivo)
    try:
        tty.setcbreak(arquivo)
        yield
    finally:
        termios.tcsetattr(arquivo, termios.TCSADRAIN, anterior)


def _ler_tecla():
    if os.name == "nt":
        import msvcrt

        tecla = msvcrt.getwch()
        if tecla in ("\x00", "\xe0"):
            msvcrt.getwch()  # Ignora setas e teclas de função.
            return ""
        return tecla

    import select

    arquivo = sys.stdin.fileno()
    tecla = os.read(arquivo, 1)
    if not tecla:
        raise EOFError
    if tecla == b"\x1b":
        # Setas e outras teclas especiais também começam com Esc no Linux.
        if select.select([arquivo], [], [], 0.05)[0]:
            while select.select([arquivo], [], [], 0.01)[0]:
                os.read(arquivo, 1)
            return ""
    return tecla.decode("ascii", errors="ignore")


def ler_opcao(mensagem=">"):
    """Esc retorna None; índices longos e -1 continuam aceitando Enter."""
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        return input(mensagem)

    texto = ""
    with _modo_teclado():
        sys.stdout.write(mensagem)
        sys.stdout.flush()
        while True:
            tecla = _ler_tecla()
            if tecla == "\x03":
                raise KeyboardInterrupt
            if tecla == "\x04":
                raise EOFError
            if tecla == "\x1b":
                sys.stdout.write("\n")
                sys.stdout.flush()
                return None
            if tecla in ("\r", "\n"):
                sys.stdout.write("\n")
                sys.stdout.flush()
                return texto
            if tecla in ("\b", "\x7f"):
                if texto:
                    texto = texto[:-1]
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                continue
            if tecla and tecla.isascii() and tecla.isprintable():
                texto += tecla
                sys.stdout.write(tecla)
                sys.stdout.flush()
