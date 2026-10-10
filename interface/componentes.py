"""Componentes Rich com bordas Unicode uniformes, preservando os emojis."""

from rich import box
from copy import copy
from rich.panel import Panel as RichPanel
from rich.table import Table as RichTable


class Table(RichTable):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("box", box.ROUNDED)
        kwargs.setdefault("padding", (0, 2))
        super().__init__(*args, **kwargs)

    def __rich_console__(self, console, options):
        tabela = copy(self)
        if tabela.width is not None:
            tabela.width = min(tabela.width, options.max_width)
        yield from RichTable.__rich_console__(tabela, console, options)


class Panel(RichPanel):
    def __init__(self, renderable, **kwargs):
        kwargs.setdefault("box", box.ROUNDED)
        kwargs.setdefault("padding", (0, 2))
        super().__init__(renderable, **kwargs)
