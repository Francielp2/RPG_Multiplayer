from jogador import Jogador
from interface.componentes import Table
from interface.componentes import Panel
from interface.io import print
from rich.text import Text
from rich.columns import Columns



def Tabelajogadores(jogadores:list[Jogador],jogatual:Jogador):

    tabela = Table(title="Jogadores", width=100, padding=(0, 1))
    tabela.add_column("", width=1)
    tabela.add_column("Nome",justify="left",style="bold",ratio=2, overflow="fold")
    tabela.add_column("[#0BC900]HP ❤️[/]",justify="center",ratio=1, overflow="fold")
    tabela.add_column("[#FFF300]Moedas ✪ [/]",justify="left",ratio=1,style="#FFF300", overflow="fold")
    tabela.add_column("🧪 Poções / rodadas restantes", ratio=3, style="green", overflow="fold")

    for jog in jogadores :
        alerta = ""
        corhp = "[#0BC900]"
        nomecor = "[bold]"
        if 20 <= jog.hp <= 30:
            corhp = "[#FFA500]"  # laranja em rgb
            nomecor = "[#FFA500]"
        elif jog.hp < 20:
            corhp = "[bold red]"
            nomecor = "[bold red]"
            alerta = "[bold red]⚠️[/]"
        marcador = "[red]▻[/]" if jog == jogatual else ""
        tabela.add_row(f"{marcador}",f"{nomecor}{jog.nome}[/]{alerta}",f"{corhp}{jog.hp}[/]",f"{jog.moedas}",jog.resumo_pocoes())
    print(tabela)


def mostrar_acoes(jogatual:Jogador,turno):
    espada = jogatual.arma if jogatual.arma else "Sem arma"
    anel = jogatual.anel if jogatual.anel else "Sem anel"
    armadura = jogatual.armadura if jogatual.armadura else "Sem armadura"
    texto = Text()
    texto.append("[1] ⚔️ Atacar\n",style="bold red")
    texto.append("[2] ▣ Loja\n",style="bold #FFF300")
    texto.append("[3] ▤ Inventário\n",style="bold blue")
    opcoesPanel = Panel(texto,width=28,title="⚔ AÇÕES")
    status = f"[#0BC900]HP : [bold]{jogatual.hp}[/][/]"
    status +=f"\n[#FFF300]Moedas ✪ : [bold]{jogatual.moedas}[/][/]"
    status += f"\n[#0EEE7E]Sorte: [bold]{jogatual.sorte_total}[/]x[/]"
    status += f"\n[red]DANO = (1 - {jogatual.d10max}) + {jogatual.dano}[/]"
    status += f"\n[blue]AGILIDADE = (1 - {jogatual.d20max}) + {jogatual.agilidade}[/]"
    status+= f"\nEspada : {espada}"
    status+=f"\nAnel   : {anel}"
    status += f"\nArmadura : {armadura}"
    status += f"\n[green]🧪 Poções ativas:\n{jogatual.resumo_pocoes()}[/]"
    statusPainel = Panel(status,
                         title=f"[bold red on black]{jogatual.nome}[/]",
                         width=64,subtitle=f"⏰ [bold red on black]Turno :{turno}[/]")
    print(Columns([opcoesPanel,statusPainel], padding=(0, 2)))



