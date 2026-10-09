from time import sleep

import interface
import som
from equipamento.armadura import Armadura
from interface.funcoes import limpar_tela
from jogador import Jogador
from equipamento import Equipamento
from combate import Combate
from partida import Partida
from loja import Loja
from rich import print
from interface.menu import mostrar_acoes,Tabelajogadores
from interface.funcoes import mostrar_mensagem
from eventos import EventoAleatorio
#emojis que funcionam no terminal : ☠️⚔️✨⚙️⛏️⏲️⏰⏳⌛
# ✏️⛲⛺♨️⛈️❄️⚠️❇️✅❌✪↩️↓↑♾️☯️✝️
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
    if jogatual >= len(jogadores): #TESTE
        jogatual = 0
    jog = jogadores[jogatual] #Jogador atual
    evento = EventoAleatorio(turno=turno,jogadores=jogadores)
    Tabelajogadores(jogadores=jogadores,jogatual=jog)
    mostrar_acoes(jog,turno=turno)
    loja.turno = turno
    #opc = Partida.validar_opc([0  , 1,2,3,4 , 5,6],"Sua opção:") pra teste
    opc = Partida.validar_opc([1, 2, 3, 4], "Sua opção:")

    #if opc == 0 : pular jogador
     #   jogatual = (jogatual + 1) % len(jogadores)
     #   turno += 1
    if opc == 1 :
        som.atacar.play()
        combate = Combate(jog=jogadores[jogatual],jogadores=jogadores,indice=jogatual)
        if combate.atacar() :
            partida.verificar_mortos()
            if partida.fim_partida():
                break
            Partida.ganhar_moeda(rodada=rodada, jog=jog)
            evento.executar()
            jogatual = (jogatual + 1) % len(jogadores) #passou para o proximo jogador

            if jogatual == 0 : #verifica se passou de rodada
                loja.chance_att_loja()
                rodada +=1
            turno += 1


    if opc == 2 :
        loja.entrar_loja(jog=jog)

    if opc == 3 :
        jogadores[jogatual].mostrar_inventario()

    if opc == 4 : #testando eventos
        evento.escolher_jogador(),evento.hp()

    if opc == 5 : #hack de moedas para testes
        jog.moedas += 20000

