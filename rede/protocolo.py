"""TCP é um fluxo: cada mensagem JSON termina em newline."""

import json
import socket
from threading import Lock


MAX_MENSAGEM = 65536


class ErroProtocolo(ValueError):
    pass


class CanalJSON:
    def __init__(self, conexao):
        self.socket = conexao
        self.buffer = bytearray()
        self.lock_envio = Lock()

    def enviar(self, mensagem):
        dados = json.dumps(mensagem, ensure_ascii=False, allow_nan=False).encode("utf-8")
        if len(dados) > MAX_MENSAGEM:
            raise ErroProtocolo("Mensagem muito grande.")
        with self.lock_envio:
            self.socket.sendall(dados + b"\n")

    def receber(self):
        while b"\n" not in self.buffer:
            if len(self.buffer) > MAX_MENSAGEM:
                raise ErroProtocolo("Mensagem muito grande.")
            dados = self.socket.recv(4096)
            if not dados:
                raise ConnectionError("Conexão encerrada.")
            self.buffer.extend(dados)
        linha, _, restante = self.buffer.partition(b"\n")
        self.buffer = bytearray(restante)
        if len(linha) > MAX_MENSAGEM:
            raise ErroProtocolo("Mensagem muito grande.")
        try:
            mensagem = json.loads(linha.decode("utf-8"))
        except (ValueError, UnicodeError) as erro:
            raise ErroProtocolo("JSON ou UTF-8 inválido.") from erro
        if not isinstance(mensagem, dict) or not isinstance(mensagem.get("tipo"), str):
            raise ErroProtocolo("A mensagem precisa de um tipo.")
        return mensagem

    def fechar(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.socket.close()
