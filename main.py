import som
from interface.funcoes import limpar_tela
from jogador import Jogador
from combate import Combate
from partida import Partida
from loja import Loja
from rich import print
from interface.menu import mostrar_acoes,Tabelajogadores
from interface.funcoes import mostrar_mensagem
from eventos import EventoAleatorio
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
partida = Partida(jogadores)

jogatual = 0
turno = 1
rodada = 1
loja = Loja()
while True :
    limpar_tela()

    partida.verificar_mortos()
    if partida.fim_partida() :
        break
    jog = jogadores[jogatual] #Jogador atual
    evento = EventoAleatorio(turno=turno,jogadores=jogadores)
    Tabelajogadores(jogadores=jogadores,jogatual=jog)
    mostrar_acoes(jog,turno=turno)
    loja.turno = turno
    opc = Partida.validar_opc([1, 2, 3, 4], "Sua opção:")

    if opc == 1 :
        ordem_turno = jogadores.copy()
        som.atacar.play()
        combate = Combate(jog=jogadores[jogatual],jogadores=jogadores,indice=jogatual)
        if combate.atacar() :
            partida.verificar_mortos()
            if partida.fim_partida():
                break
            Partida.ganhar_moeda(rodada=rodada, jog=jog)
            evento.executar()
            partida.verificar_mortos()
            if partida.fim_partida():
                break
            proximo, fim_rodada = partida.proximo_jogador(jog, ordem_turno)
            jogatual = jogadores.index(proximo)

            if fim_rodada:
                partida.encerrar_rodada()
                loja.chance_att_loja()
                rodada +=1
            turno += 1


    if opc == 2 :
        loja.entrar_loja(jog=jog)

    if opc == 3 :
        jogadores[jogatual].mostrar_inventario()
