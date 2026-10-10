from os import remove
from random import randint
from time import sleep

from interface.componentes import Panel
from interface.componentes import Table

import som
from equipamento import Equipamento
from equipamento.armadura import Armadura
from interface.funcoes import mostrar_mensagem
from rich import print
class Jogador :
    def __init__(self,nome,hp):
        # ========= ATRIBUTOS ========
        self.nome = nome
        self.hp = hp
        self.danobonus = 0
        self.agilidadebonus = 0
        self.moedas = 0 #original = 0
        self.sorte = 1.0 #original = 1.0
        self.inventario = []

        # ========= SLOTS ========
        self.arma:Equipamento = None
        self.anel:Equipamento = None
        self.armadura:Armadura = None


    @property
    def agilidade(self):
        """Calcula todo o bonus de agilidade do jogador"""
        agi = self.agilidadebonus
        if self.anel :
            agi += self.anel.agilidade
        if  self.arma:
            agi += self.arma.agilidade
        return agi

    @property
    def d20max(self):
        """A cada 10 de bonus de agilidade aumenta 1 no valor máximo do d20"""
        return min(20+ self.agilidade // 10, 30) #a cada 10 de bonus de agilidade aumenta 1 no dado d20
    #começa com 20, o máximo é 30. aumenta as chances de crítico

    @property
    def d10max(self):
        dmax = 10 #começa com 10 sendo o maior valor do dado no inicio
        if self.arma :
            dmax += self.arma.dano
        return dmax


    @property
    def dano(self):
        """Pega os bonus de ataque, sem contar da arma, pois o bonus da arma
        vai influenciar o dado, ele não vai somar, apenas o dano do anel e o
        bonus que vai somar"""
        dano = self.danobonus
        if self.anel :
            dano += self.anel.dano
        return dano

    def receber_dano(self,dano,combate=False):
        if self.armadura :
            dano = self.armadura.absorverDano(dano)

            if self.armadura.esta_quebrada() :
                self.inventario.remove(self.armadura)
                self.armadura = None
        texto = f"{self.nome} perdeu [bold]{dano} de HP![/]"
        texto += f"\n{self.nome} HP: {self.hp} -> "
        self.hp = max(0, self.hp - dano)
        texto += f"{self.hp}"
        if combate :
            mostrar_mensagem(mensagem=texto,
                             titulo="DANO", estilo="red",
                             largura=35, pausa=0.8,som=som.dano_som(dano))
        else :
            mostrar_mensagem(mensagem=texto,
                             titulo="DANO", estilo="red",
                             largura=35, pausa=0.8)
        sleep(2)
        return dano



    # ============ CALCULANDO AGILIDADE DADO D20===========
    def d20 (self) :
        return randint(1,self.d20max) #original (1,20)

    def agilidadetot(self,d20):
        texto = ""
        agitot = d20
        texto = "Rolando dado de agilidade🎲..."
        texto += f"\n[bold] {d20}[/]"
        if self.agilidadebonus > 0 :
            texto += f"\n+[bold]{self.agilidadebonus}[/] Agilidade bonus"
            agitot += self.agilidadebonus
        if self.anel and self.anel.agilidade > 0 :
            texto += f"\n+[bold]{self.anel.agilidade}[/] Agilidade do [bold]{self.anel.nome}[/]"
            agitot += self.anel.agilidade
        if d20 != agitot :
            texto += f"\n[bold]TOTAL = {agitot}[/]"
        mostrar_mensagem(mensagem=texto,titulo="DADO DE AGILIDADE🎲",
                         largura=35,estilo="blue",pausa=0.7,som=som.dado,linha_som=2)
        sleep(1)
        return agitot

    # ============calculando dano dado D10===========
    def d10 (self) :
        return randint(1,self.d10max) #original (1,10)


    def danotot (self,d10,d20) :
        texto = ""
        texto += "Rolando dado de ataque🎲..."
        texto += f"\n [bold]{d10}[/]"
        danotot = d10
        if self.danobonus >0 :
            texto += f"\n+{self.danobonus} de bônus de ataque"
            danotot += self.danobonus
        if self.anel and self.anel.dano > 0 :
            danotot += self.anel.dano
            texto += f"\n+{self.anel.dano} de ataque do {self.anel.nome}"
        if d20 >= 20 :
            mostrar_mensagem(mensagem="[bold red on black]ESPECIAL ATIVADO!!![/]",
                             titulo="DADO DE ATAQUE🎲", estilo="red",
                             pausa=1, largura=35, som=som.especial)
            danotot *= 2
        if d10 != danotot :
            texto += f"\n[bold]DANO TOTAL = {danotot}[/]"

        mostrar_mensagem(mensagem=texto,
                         titulo="DADO DE ATAQUE🎲",estilo="red",
                         pausa=0.8, largura=35,som=som.dado,linha_som=2)
        sleep(0.9)
        return danotot


    def roletar_sorte(self,probabilidade=45):
        chance = int(probabilidade * self.sorte)
        return randint(1,100) <= chance #retorna true ou false

    def aumentar_sorte(self,valor=0.1) :
        self.sorte = round(min(self.sorte + valor,2.0),1)


    #============ INVENTÁRIO===========
    def adicionar_item_inventario(self,item) :
        mostrar_mensagem(mensagem=f"[bold]{item}[/] foi adicionado no inventário ▤ ",
                         titulo="▤ INVENTÁRIO",pausa=1.5,largura=35)
        self.inventario.append(item)

    def mostrar_inventario(self):
        som.inventario.play()
        if not self.inventario :
            mostrar_mensagem(mensagem="Inventário vazio",titulo="▤ Inventário",
                             estilo="red",pausa=1.5)
            return
        while self.inventario:
            tabela = Table(title="▤ Inventário ▤ ", width=88)
            tabela.add_column("#")  # index
            tabela.add_column("Nome", ratio=2)
            tabela.add_column("Dano",style="red")
            tabela.add_column("Agilidade",style="blue")
            tabela.add_column("defesa",style="steel_blue")
            tabela.add_column("Categoria")
            tabela.add_column("Venda ✪", style="#FFF300")
            from partida import Partida
            for i, item in  enumerate(self.inventario) :
                tabela.add_row(
                    str(i),
                    str(item),
                    str(item.dano if item.dano > 0 else " _ "),
                    str(item.agilidade if item.agilidade > 0 else " _ "),
                    str(item.defesa if item.defesa > 0 else " _ "),
                    str(item.tipo),
                    str(self.preco_venda(item))
                )
            tabela.add_row("[red]-1[/]", "[red]↩️ Voltar[/]", "", "", "", "", "")
            print(tabela)
            arma = self.arma if self.arma else "Vazio"
            anel = self.anel if self.anel else "Vazio"
            armadura = self.armadura if self.armadura else "Vazio"
            texto = f"Arma : {arma}"
            texto += f"\nAnel : {anel}"
            texto += f"\nArmadura: {armadura}"
            painel = Panel(title="EQUIPADOS⚔️",
                           renderable=texto,width=76)
            print(painel)

            opc = Partida.validar_opc(lista=self.inventario)
            if opc == None :
                return

            item = self.inventario[opc]
            if isinstance(item, Equipamento):
                acoes = (f"{item}\n"
                         "[green][0] ↑ Equipar[/]\n"
                         "[blue][1] ↓ Desequipar[/]\n"
                         f"[#FFF300][2] Vender por {self.preco_venda(item)} moeda(s)[/]\n"
                         "[red][-1] ↩️ Voltar[/]")
                print(Panel(acoes, title="▤ AÇÕES DO ITEM", width=76))
                acao = Partida.validar_opc([0, 1, 2], "Sua opção: ")
                if acao == 0:
                    self.equipar(item)
                elif acao == 1:
                    self.desequipar(item)
                elif acao == 2:
                    self.vender(item)


    def equipar(self,item):
        texto = ""
        if item not in self.inventario :
            mostrar_mensagem(f"{item} Não está no inventário",titulo=":/",estilo="red")
            sleep(1)
            return
        if item.tipo == 'arma' :
            if self.arma :
                texto = f"↓ Desequipando {self.arma}\n"
            self.arma = item
        elif item.tipo == "anel" :
            if self.anel :
                texto = f"↓ Desequipando {self.anel}\n"
                sleep(0.5)
            self.anel = item

        elif item.tipo == "armadura":
            if self.armadura:
                texto = f"↓ Desequipando {self.armadura.nome}\n"
            self.armadura = item
        texto += f"[bold]{self.nome}[/]↑ Equipou [bold]{item}[/]"
        som.equipar.play()
        mostrar_mensagem(texto,titulo="▤ Inventário",pausa=1.3,largura=50)

    @staticmethod
    def preco_venda(item):
        return max(1, int(item.valor * 0.25))

    def desequipar(self, item, anunciar=True):
        for slot in ("arma", "anel", "armadura"):
            if getattr(self, slot) is item:
                setattr(self, slot, None)
                if anunciar:
                    som.equipar.play()
                    mostrar_mensagem(f"[bold]{self.nome}[/] ↓ Desequipou {item}",
                                     titulo="▤ Inventário", pausa=1.3, largura=50)
                return True
        if anunciar:
            mostrar_mensagem(f"{item} não está equipado!", titulo="▤ Inventário",
                             estilo="red", largura=50)
        return False

    def vender(self, item):
        if item not in self.inventario:
            mostrar_mensagem(f"{item} não está no inventário!", titulo="▤ Inventário",
                             estilo="red", largura=50)
            return False
        valor = self.preco_venda(item)
        self.desequipar(item, anunciar=False)
        self.inventario.remove(item)
        self.moedas += valor
        som.moedas.play()
        mostrar_mensagem(f"{self.nome} vendeu {item} por {valor} moeda(s)!"
                         f"\nMoedas ✪: {self.moedas}", titulo="▤ VENDA",
                         estilo="#FFF300", pausa=1.3, largura=70)
        return True
