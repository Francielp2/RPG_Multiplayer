"""Sockets recebem respostas; somente a thread do motor altera a partida."""

from dataclasses import dataclass
import socket
import traceback
from threading import Condition, Event, Thread
from time import monotonic
from uuid import uuid4

from rich.markup import escape

from rede.protocolo import CanalJSON, ErroProtocolo
from rede.terminal_remoto import TerminalRemoto


class SessaoEncerrada(Exception):
    pass


@dataclass
class Sessao:
    id: str
    nome: str
    largura: int
    canal: CanalJSON


class Servidor:
    def __init__(self, host="0.0.0.0", porta=5000, jogadores=2, timeout=120,
                 hp=100, fator_pausa=1.0):
        self.host, self.porta = host, porta
        self.quantidade = jogadores
        self.timeout = timeout
        self.hp = hp
        self.fator_pausa = fator_pausa
        self.sessoes = []
        self.condicao = Condition()
        self.encerrado = Event()
        self.pronto = Event()
        self.motivo = None
        self.pedido = None
        self.resposta = None
        self.partida = None
        self.threads = []

    def enviar(self, mensagem, destinatario=None):
        for sessao in list(self.sessoes):
            if destinatario is None or sessao.id == destinatario:
                try:
                    sessao.canal.enviar(mensagem)
                except (OSError, ErroProtocolo) as erro:
                    self.abortar(f"{sessao.nome} desconectou: {erro}")
        if self.encerrado.is_set() and mensagem["tipo"] != "fim_partida":
            raise SessaoEncerrada(self.motivo)

    def abortar(self, motivo):
        with self.condicao:
            if not self.encerrado.is_set():
                self.motivo = motivo
                self.encerrado.set()
                self.condicao.notify_all()

    def aguardar(self, segundos):
        if self.encerrado.wait(segundos):
            raise SessaoEncerrada(self.motivo)

    def _receber(self, sessao):
        while not self.encerrado.is_set():
            try:
                mensagem = sessao.canal.receber()
            except socket.timeout:
                continue
            except (OSError, ErroProtocolo) as erro:
                self.abortar(f"{sessao.nome} desconectou ou enviou mensagem inválida: {erro}")
                return
            valor = mensagem.get("valor")
            with self.condicao:
                valido = (mensagem.get("tipo") == "resposta"
                          and set(mensagem) == {"tipo", "pedido_id", "valor"}
                          and (valor is None or isinstance(valor, str) and len(valor) <= 64
                               and all(letra.isprintable() for letra in valor))
                          and self.pedido is not None
                          and self.pedido["jogador_id"] == sessao.id
                          and self.pedido["pedido_id"] == mensagem.get("pedido_id")
                          and self.resposta is None)
                if valido:
                    self.resposta = mensagem
                    self.condicao.notify_all()
            if not valido:
                try:
                    sessao.canal.enviar({"tipo": "erro", "texto": "Resposta recusada: não é sua vez, solicitação antiga ou conteúdo inválido."})
                except OSError:
                    self.abortar(f"{sessao.nome} desconectou.")

    def perguntar(self, jogador_id, texto, cancelavel, privado=False):
        sessao = next(sessao for sessao in self.sessoes if sessao.id == jogador_id)
        pedido_id = uuid4().hex
        with self.condicao:
            self.pedido = {"pedido_id": pedido_id, "jogador_id": jogador_id}
            self.resposta = None
        for destino in self.sessoes:
            if not privado or destino.id == jogador_id:
                self.enviar({"tipo": "solicitar_entrada", "pedido_id": pedido_id,
                             "jogador_id": jogador_id, "nome": sessao.nome,
                             "texto": texto, "cancelavel": cancelavel,
                             "responder": destino.id == jogador_id}, destino.id)
        limite = monotonic() + self.timeout
        with self.condicao:
            while self.resposta is None and not self.encerrado.is_set():
                restante = limite - monotonic()
                if restante <= 0:
                    self.abortar(f"Tempo de resposta esgotado para {sessao.nome}.")
                    break
                self.condicao.wait(restante)
            resposta = self.resposta
            self.pedido = None
            self.resposta = None
        if self.encerrado.is_set():
            raise SessaoEncerrada(self.motivo)
        valor = resposta["valor"]
        # Cancelar uma aposta equivale à opção existente de apostar zero.
        if valor is None and not cancelavel:
            valor = "0"
        if not privado:
            self.enviar({"tipo": "aviso", "texto": f"{sessao.nome} respondeu: {'Esc' if valor is None else valor}"})
        return valor

    def _lobby(self, escuta):
        limite = monotonic() + self.timeout
        while len(self.sessoes) < self.quantidade:
            if self.encerrado.is_set():
                raise SessaoEncerrada(self.motivo)
            if monotonic() >= limite:
                raise SessaoEncerrada("Tempo esgotado aguardando jogadores no lobby.")
            try:
                conexao, _ = escuta.accept()
            except socket.timeout:
                continue
            canal = CanalJSON(conexao)
            conexao.settimeout(min(10, self.timeout))
            try:
                mensagem = canal.receber()
                nome = mensagem.get("nome")
                largura = mensagem.get("largura", 100)
                if (mensagem.get("tipo") != "entrar" or not isinstance(nome, str)
                        or not 1 <= len(nome.strip()) <= 30
                        or not all(letra.isprintable() for letra in nome)
                        or type(largura) is not int or not 40 <= largura <= 160):
                    raise ErroProtocolo("Nome (1–30 caracteres) ou largura inválidos.")
                nome = escape(nome.strip())
                if any(sessao.nome.casefold() == nome.casefold() for sessao in self.sessoes):
                    raise ErroProtocolo("Este nome já está em uso.")
                sessao = Sessao(f"j{len(self.sessoes) + 1:03}", nome, largura, canal)
                conexao.settimeout(1)
                self.sessoes.append(sessao)
                canal.enviar({"tipo": "bem_vindo", "jogador_id": sessao.id, "nome": nome})
                leitor = Thread(target=self._receber, args=(sessao,), daemon=True)
                leitor.start()
                self.threads.append(leitor)
                self.enviar({"tipo": "aviso", "texto": f"Lobby: {nome} entrou ({len(self.sessoes)}/{self.quantidade})."})
                limite = monotonic() + self.timeout
            except (OSError, ErroProtocolo) as erro:
                try:
                    canal.enviar({"tipo": "erro", "texto": str(erro)})
                except OSError:
                    pass
                canal.fechar()

    def rodar(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as escuta:
            escuta.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            escuta.bind((self.host, self.porta))
            escuta.listen(self.quantidade)
            escuta.settimeout(.5)
            self.porta = escuta.getsockname()[1]
            print(f"Servidor em {self.host}:{self.porta}; aguardando {self.quantidade} jogadores.", flush=True)
            self.pronto.set()
            try:
                self._lobby(escuta)
                # Uma sala por processo; conexões extras são recusadas pelo SO.
                escuta.close()
                from interface.io import usar_terminal
                from jogador import Jogador
                from partida.motor import executar_partida

                jogadores = [Jogador(sessao.nome, self.hp, jogador_id=sessao.id) for sessao in self.sessoes]
                terminal = TerminalRemoto(self, min(sessao.largura for sessao in self.sessoes), self.fator_pausa)
                self.enviar({"tipo": "inicio_partida", "jogadores": [
                    {"id": jog.id, "nome": jog.nome} for jog in jogadores]})
                with usar_terminal(terminal):
                    self.partida = executar_partida(jogadores)
                vencedor = jogadores[0].id if len(jogadores) == 1 else None
                self.enviar({"tipo": "fim_partida", "vencedor_id": vencedor,
                             "texto": "Partida encerrada.", "cancelada": False})
            except (SessaoEncerrada, KeyboardInterrupt) as erro:
                texto = str(erro) or "Servidor interrompido."
                self.enviar({"tipo": "fim_partida", "vencedor_id": None,
                             "texto": texto, "cancelada": True})
            except Exception:
                # O diagnóstico fica no servidor; clientes saem da entrada pendente.
                traceback.print_exc()
                self.enviar({"tipo": "fim_partida", "vencedor_id": None,
                             "texto": "Erro no servidor; consulte o terminal do servidor.",
                             "cancelada": True})
            finally:
                self.encerrado.set()
                for sessao in self.sessoes:
                    sessao.canal.fechar()
                for leitor in self.threads:
                    leitor.join(timeout=2)
