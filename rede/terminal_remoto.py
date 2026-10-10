"""Renderiza os componentes originais uma vez e transmite o mesmo ANSI."""

from contextlib import contextmanager
from io import StringIO

from rich.console import Console


class TerminalRemoto:
    def __init__(self, servidor, largura, fator_pausa=1.0):
        self.servidor = servidor
        self.largura = largura
        self.fator_pausa = fator_pausa
        self.atual = None
        self.destinatario = None

    def mostrar(self, *objetos, **opcoes):
        saida = StringIO()
        console = Console(file=saida, width=self.largura, force_terminal=True,
                          color_system="truecolor", highlight=False)
        console.print(*objetos, **opcoes)
        self.servidor.enviar({"tipo": "tela", "conteudo": saida.getvalue()}, self.destinatario)

    def limpar(self):
        self.servidor.enviar({"tipo": "limpar"}, self.destinatario)

    def pausa(self, segundos):
        self.servidor.aguardar(segundos * self.fator_pausa)

    def perguntar(self, mensagem, jogador=None, cancelavel=False):
        jogador = jogador or self.atual
        return self.servidor.perguntar(jogador.id, mensagem, cancelavel,
                                       privado=self.destinatario is not None)

    def atualizar_estado(self, jogadores, atual, turno, rodada):
        self.atual = atual
        self.servidor.enviar({
            "tipo": "estado", "atual_id": atual.id, "turno": turno, "rodada": rodada,
            "jogadores": [{"id": jog.id, "nome": jog.nome, "hp": jog.hp,
                           "moedas": jog.moedas, "sorte": jog.sorte_total,
                           "pocoes": jog.resumo_pocoes()}
                          for jog in jogadores],
        })

    def anunciar(self, texto):
        self.servidor.enviar({"tipo": "aviso", "texto": texto})

    @contextmanager
    def privado(self, jogador):
        anterior = self.destinatario
        self.destinatario = jogador.id
        try:
            yield
        finally:
            self.destinatario = anterior
