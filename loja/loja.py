from rich.columns import Columns
from interface.componentes import Panel

from equipamento.armadura import Armadura
from equipamento.pocao import Pocao
from equipamento import Equipamento
from interface.funcoes import mostrar_mensagem, limpar_tela
from interface.teclado import ler_opcao
from jogador import Jogador
from random import randint,random
from time import sleep
from rich import print
from interface.componentes import Table
import som
class Loja:
    def __init__(self):
        self.estoque: list[Equipamento] = []
        self.slot = 3
        self.preco_slot = 2
        self.turno = 1

    def entrar_loja(self,jog:Jogador):
        while True :
            limpar_tela()
            self.mostrar_loja(jog)
            if not self.compra(jog) :
                break


    def tem_moeda (self,jog:Jogador,valor):
        if jog.moedas < valor :
            print("[red bold]Moedas insuficiente![/]")
            sleep(0.6)
            return False

        jog.moedas -= valor
        return True

    def novo_equip(self):
        chance = random()
        if chance < 0.51 :
            equip = Equipamento.gerarArma(self.turno)
        elif chance < 0.765 :
            equip = Equipamento.gerarAnel(self.turno)
        elif chance < 0.85:
            equip = Armadura.gerarArmadura(self.turno)
        else:
            equip = Pocao.gerarPocao()
        self.estoque.append(equip)

    def att_loja(self):
        som.attloja.play()
        mostrar_mensagem("❇️LOJA ATUALIZADA!❇️",
                         estilo="#FFF300",titulo="LOJA")
        self.estoque = []
        for c in range (0,self.slot) :
            self.novo_equip()

    def chance_att_loja(self) :
        chance = random()
        if chance < 0.38 :
            self.att_loja()
        return

    def mostrar_loja(self,jog:Jogador):
        tabelaarma = Table(title="[#FFF300] ⚔️ ARMAS⚔️ [/] ", width=76)
        tabelaarma.add_column("#") #indice
        tabelaarma.add_column("Nome", ratio=2)
        tabelaarma.add_column("Dano", style="red")
        tabelaarma.add_column("Agilidade", style="blue")
        tabelaarma.add_column("Preço", style="#FFF300")


        tabelaanel = Table(title="[blue]ANEIS[/]", width=76)
        tabelaanel.add_column("#")  # indice
        tabelaanel.add_column("Nome", ratio=2)
        tabelaanel.add_column("Dano", style="red")
        tabelaanel.add_column("Agilidade", style="blue")
        tabelaanel.add_column("Preço", style="#FFF300")

        tabelaarmadura = Table(title="ARMADURAS", width=76)
        tabelaarmadura.add_column("#")  # indice
        tabelaarmadura.add_column("Nome", ratio=2)
        tabelaarmadura.add_column("Defesa",style="steel_blue")
        tabelaarmadura.add_column("Preço", style="#FFF300")

        tabelapocao = Table(title="[green]🧪 POÇÕES[/]", width=76, padding=(0, 1))
        tabelapocao.add_column("#")
        tabelapocao.add_column("Nome", ratio=2, overflow="fold")
        tabelapocao.add_column("Efeito", overflow="fold")
        tabelapocao.add_column("Duração", overflow="fold")
        tabelapocao.add_column("Preço", style="#FFF300")

        if self.estoque :
            for i, e in enumerate (self.estoque) : # e-> equipamento
                if e.tipo =="arma" :
                    tabelaarma.add_row(str(i),
                                       str(e),
                                       str(e.dano),
                                       str(e.agilidade),
                                       str(e.valor), )
                elif e.tipo == "anel" :
                    tabelaanel.add_row(str(i),
                                       str(e),
                                       str(e.dano),
                                       str(e.agilidade),
                                       str(e.valor), )
                elif e.tipo == "armadura" :
                    tabelaarmadura.add_row(str(i),
                                           str(e),
                                           str(e.defesa),
                                           str(e.valor))
                elif isinstance(e, Pocao):
                    tabelapocao.add_row(str(i), str(e), e.descricao_efeito,
                                       e.descricao_duracao, str(e.valor))
            print(Columns([tabelaarma,tabelaanel,tabelaarmadura,tabelapocao], padding=(0, 2)))

        else :
            mostrar_mensagem(mensagem="[red]Nenhum equipamento disponível na loja![/]",
                             titulo="[#FFF300] ▣ LOJA ▣ [/]",pausa=0)
        print("-="*30)
        texto = f"[#2ECC71][-3] ✚ Comprar +1 slot[/] [#FFF300]({self.preco_slot} moedas)[/]"
        texto += f"\n[#3498DB][-2] ✨ Atualizar loja[/] [#FFF300](5 moedas)[/]"
        texto += f"\n[red][-1] ↩️ Voltar[/]"
        texto +=f"\n[#FFF300]Suas [bold]moedas ✪ : {jog.moedas}[/][/]"
        painel = Panel(texto,title="suas ações :",width=76)
        print(painel)

    def compra(self, jog: Jogador):
        while True :
            try :
                entrada = ler_opcao("sua opção : ")
                if entrada is None:
                    return
                indice = int(entrada)
                if indice in (-3,-2,-1) : #comprar slot,att loja ou sair, é válido
                    break #valor válido, pode continuar

                if 0 <= indice < len(self.estoque) :
                    break #valor válido, pode continuar

            except ValueError :
                print("[red]Digite um valor válido[/]")

        if indice == -1 :
            return #sair da loja

        elif indice == -2 :
            if self.tem_moeda(valor=5,jog=jog) : #verifica se o jogador tem dinheiro pra att loja
                self.att_loja()

        elif indice == -3 : #comprar slot na loja
            if self.tem_moeda(jog=jog,valor=self.preco_slot) :
                som.novo_slot.play()
                self.slot += 1
                self.preco_slot += 1
                self.novo_equip()
        else :
            if self.tem_moeda(jog=jog,valor=self.estoque[indice].valor) :
                som.compra.play()
                jog.adicionar_item_inventario(self.estoque[indice])
                self.estoque.remove(self.estoque[indice])
        return True


