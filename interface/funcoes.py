from interface.io import print
from interface.componentes import Panel
from interface.io import pausa as sleep
from interface.io import limpar

def limpar_tela():
    limpar()

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
