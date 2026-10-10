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


class EntradaInterrompida(Exception):
    """Permite restaurar o terminal quando uma sessão remota acaba."""


def _ler_tecla(cancelamento=None):
    if os.name == "nt":
        import msvcrt

        if cancelamento is not None:
            while not msvcrt.kbhit():
                if cancelamento.wait(.05):
                    raise EntradaInterrompida
        tecla = msvcrt.getwch()
        if tecla in ("\x00", "\xe0"):
            msvcrt.getwch()  # Ignora setas e teclas de função.
            return ""
        return tecla

    import select

    arquivo = sys.stdin.fileno()
    if cancelamento is not None:
        while not select.select([arquivo], [], [], .1)[0]:
            if cancelamento.is_set():
                raise EntradaInterrompida
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


def ler_opcao(mensagem=">", cancelamento=None):
    """Esc retorna None; índices longos e -1 continuam aceitando Enter."""
    from interface.io import terminal_atual

    terminal = terminal_atual()
    if terminal is not None:
        return terminal.perguntar(mensagem, cancelavel=True)
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        if cancelamento is not None and os.name != "nt":
            import select
            sys.stdout.write(mensagem)
            sys.stdout.flush()
            while not select.select([sys.stdin], [], [], .1)[0]:
                if cancelamento.is_set():
                    raise EntradaInterrompida
            linha = sys.stdin.readline()
            if not linha:
                raise EOFError
            return linha.rstrip("\r\n")
        return input(mensagem)

    texto = ""
    with _modo_teclado():
        sys.stdout.write(mensagem)
        sys.stdout.flush()
        while True:
            if cancelamento is not None and cancelamento.is_set():
                raise EntradaInterrompida
            tecla = _ler_tecla() if cancelamento is None else _ler_tecla(cancelamento)
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
