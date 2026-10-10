from interface.funcoes import mostrar_mensagem
from interface.io import print
from partida import Partida
from partida.motor import executar_partida
from jogador import Jogador


while True :
    try :
        qj = int (input ("Quantos jogadores teremos na partida?"))
        if qj <= 1 :
            mostrar_mensagem("Só é possível iniciar uma partida com 2 ou mais jogadores  ",
                             titulo=":/",estilo="red")
        else :
            break
    except ValueError :
        print("Digite um valor válido")

jogadores : list[Jogador] = Partida.registrar_jogadores(qj=qj,hp=100)
executar_partida(jogadores)
