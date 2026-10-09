from rich import print
from rich.panel import Panel
from time import sleep
import os

def limpar_tela() :
    os.system("cls")

def mostrar_mensagem(mensagem,titulo,pausa=0.8,largura=30,estilo="",som=None,linha_som =1) :
    linhas = mensagem.split("\n")
    texto = ""
    for numlinha ,linha in enumerate( linhas,start=1) :
        texto += linha + "\n"
        limpar_tela()

        print(Panel(
            renderable=texto,title=titulo,width=largura,style=estilo
        ))


        if som and numlinha ==linha_som :
            som.play()
        sleep(pausa)
