"""Cliente leve: exibe o terminal do servidor e devolve apenas entradas."""

from queue import Queue
import socket
import sys
from threading import Event, Thread

from rich.text import Text
from rich.console import Console

from interface.teclado import EntradaInterrompida, ler_opcao
from rede.protocolo import CanalJSON, ErroProtocolo
from rede.audio_cliente import AudioCliente


def executar_cliente(host, porta, nome, largura, som=True):
    conexao = socket.create_connection((host, porta), timeout=10)
    conexao.settimeout(1)
    canal = CanalJSON(conexao)
    fila = Queue()
    encerrado = Event()
    console = Console(highlight=False)
    audio = AudioCliente(habilitado=som)

    def receber():
        while not encerrado.is_set():
            try:
                mensagem = canal.receber()
            except socket.timeout:
                continue
            except (OSError, ErroProtocolo) as erro:
                encerrado.set()
                fila.put({"tipo": "fim_partida", "texto": f"Conexão encerrada: {erro}"})
                return
            fila.put(mensagem)
            if mensagem["tipo"] == "fim_partida":
                encerrado.set()
                return

    leitor = Thread(target=receber, daemon=True)
    try:
        canal.enviar({"tipo": "entrar", "nome": nome, "largura": largura})
        leitor.start()
        while True:
            mensagem = fila.get()
            tipo = mensagem["tipo"]
            if tipo == "limpar":
                if sys.stdout.isatty():
                    console.clear(home=True)
            elif tipo == "tela":
                # Rich adapta as cores para o console Windows e para saída redirecionada.
                console.print(Text.from_ansi(mensagem["conteudo"]), end="", soft_wrap=True)
            elif tipo == "som":
                audio.executar(mensagem)
            elif tipo in ("aviso", "erro"):
                print(mensagem["texto"])
            elif tipo == "bem_vindo":
                print(f"Você é {mensagem['nome']} ({mensagem['jogador_id']}). Aguardando a sala...")
            elif tipo == "solicitar_entrada":
                if mensagem["responder"]:
                    try:
                        valor = ler_opcao(mensagem["texto"], cancelamento=encerrado)
                    except EntradaInterrompida:
                        continue
                    if not encerrado.is_set():
                        canal.enviar({"tipo": "resposta", "pedido_id": mensagem["pedido_id"], "valor": valor})
                else:
                    print(f"{mensagem['texto']} [aguardando {mensagem['nome']}]")
            elif tipo == "fim_partida":
                print(mensagem["texto"])
                return mensagem
            sys.stdout.flush()
    finally:
        encerrado.set()
        canal.fechar()
        audio.fechar()
        if leitor.is_alive():
            leitor.join(timeout=2)
