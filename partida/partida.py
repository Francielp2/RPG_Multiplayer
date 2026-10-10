import random
from time import sleep
from rich import print

import som
from interface.funcoes import mostrar_mensagem
from jogador import Jogador
class Partida :
    def __init__(self,jogadores:list[Jogador]):
        self.jogadores = jogadores
        self.mortos:list[Jogador] = []

    @classmethod
    def registrar_jogadores(cls,qj,hp):
        jogadores = []
        for i in range(qj):
            nome = str (input (f"Nome do jogador {i+1}: ")).strip().title()
            jogadores.append(Jogador(nome, hp))
        return jogadores

    def verificar_mortos (self) :
        for jogador in self.jogadores[:] :
            if jogador.hp <=0 :
                som.mortesom()
                mostrar_mensagem(f"{jogador.nome} morreu",titulo="☠️",estilo="red",
                                 pausa=2)
                self.mortos.append(jogador)
                self.jogadores.remove(jogador)

    def proximo_jogador(self, jogador_atual, ordem_turno):
        """Escolhe o próximo sobrevivente pela ordem anterior às eliminações.

        Também informa se cruzou o fim da rodada, mesmo que o primeiro
        participante ou o jogador atual tenha morrido.
        """
        if not self.jogadores:
            return None, False
        indice = ordem_turno.index(jogador_atual)
        for passo in range(1, len(ordem_turno) + 1):
            posicao = indice + passo
            candidato = ordem_turno[posicao % len(ordem_turno)]
            if candidato in self.jogadores:
                return candidato, posicao >= len(ordem_turno)

    def lista_mortos(self): #testando
        if self.mortos :
            print("Lista de mortos :")
            for morto in self.mortos :
                print(morto.nome)
    @classmethod
    def ganhar_moeda(cls,jog:Jogador,rodada):
        moedamax = int(4 + rodada / 2)
        moeda = random.randint(1,moedamax)
        chance = random.random()
        if chance < 0.35 :
            som.moedas.play()
            mostrar_mensagem(f"{jog.nome} ganhou {moeda} moedas!",estilo="#FFF300",
                             pausa=1,titulo="RECOMPENSA")
            jog.moedas += moeda
            sleep(1.5)
    def fim_partida (self):
        if len(self.jogadores) ==1 :
            if self.jogadores[0].hp >= 1 :
                campeao:Jogador = self.jogadores[0]
                som.vitoria.play()
                mostrar_mensagem(f"[#FFF300 bold]{campeao.nome}[/] [#0EEE7E]Venceu a partida![/]",pausa=2,
                                 titulo="[#FFF300 bold]VENCEDOR[/]✨")
            return True
        elif len(self.jogadores) == 0 :
            mostrar_mensagem(f"Não há vencedores...\ntodo mundo morreu☠️", titulo="☠️", estilo="red",
                             pausa=2,som=som.todos_morte,linha_som=2)
            return True

        return False

    @classmethod
    def validar_opc(cls,lista=None,mensagem=">",mnsgvazio="lista vazia"):
        if not lista:
            print(mnsgvazio)
            return None
        fim = len(lista)
        opc = None
        while opc != -1:
            try :
                opc = int (input(mensagem))
                if opc == -1 :
                    return None
                if opc >=0 and opc < fim :
                    return  opc
            except ValueError :
                print("[red]Digite um valor válido[/]")





