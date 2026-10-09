import random
from random import choice,choices
class Equipamento :
    cores_raridade = {
        None: "[bold]",
        "comum": "[bold]",
        "raro": "[blue]",
        "épico": "[purple]",
        "lendário": "[#FFEB00]",
        "mítico": "[#FF1812 bold on black]"
    }
    def __init__(self,nome,dano=0,valor=0,agilidade=0,tipo=None,raridade=None):
        self.nome = nome
        self.dano = dano
        self.valor = valor
        self.agilidade = agilidade
        self.tipo = tipo  #arma  anel  armadura
        self.defesa = 0
        self.raridade = raridade

        # ============================= GERAR ARMA ===========================

    def __str__(self):
        return f"{Equipamento.cores_raridade[self.raridade]}{self.nome}[/]"
    @classmethod
    def gerarArma(cls,turno=5,raridade=None):

        qualidade ={
            "comum": 0.3,
            "raro": 0.6,
            "épico": 1.1,
            "lendário": 1.7,
            "mítico":2
        }

        pesos = [70, 32, 9, 2, 0.4] #pesos = [70, 32, 9, 2, 0.4]
        if raridade == None :
            raridade = choices (list(qualidade.keys()),
                                weights= pesos,
                                k=1
                                )[0]
        danomin = 1
        danomax = int(qualidade[raridade] * turno)
        match raridade:
            case "comum" :
                nomes = ["espada de madeira", "graveto", "faca",
                         "Machado enferrujado", "canivete", "Espada Curta",
                         "foice velha","estilingue"]
                nome = choice(nomes).title()
            case "raro" :
                nomes = ["Espada de Prata","faca de prata","espada de ferro",
                         "Machado de batalha","foice lunar","adaga sombria",
                         "faca de prata","espada serrilhada","katana"]
                nome = choice(nomes).title()
            case "épico":
                nomes = ["Espada Flamejante","espada do trovão",
                         "machado do colosso","Foice do Ceifador☠️",
                         "Foice Sangrenta","adaga do assasino☠️",
                         "adaga das sombras","espada dourada",
                         "machado flamejante","katana do dragão☯️"]
                nome = choice(nomes).title()
                danomin = int(danomax * 0.25)
            case "lendário":
                nomes = ["Foice do Ceifador", "katana do dragão☯️",
                         "espada do dragão","Machado Leviatã",
                         "Lâminas do Caos☠️","Lâmina do Olimpo♾️",
                         "Tridente de Poseidon","Machado do Titã",
                         "foice da morte☠️","Katana do Imperador"]
                nome = choice(nomes).title()
                danomin = int(danomax * 0.50)
            case "mítico":
                nomes = ["Lâminas do Caos☠️", "Lâmina do Olimpo♾️",
                         "Tridente de Poseidon","Deus Ex Machina♾️",
                         "Olho do Apocalipse☠️","Eclipse Eterno☠️","Excalibur",
                         "Foice da Lua Negra"]
                nome = choice(nomes).title()
                danomin = int(danomax * 0.80)
        if danomin <= 0 or danomax <= 0 :
            danomin = 1
            danomax = 2
        dano = random.randint(danomin,danomax)
        valor = int(dano * 0.7)
        if valor <= 0: valor = 1
        agilidade = 0
        tipo ="arma"
        return cls(
            nome=nome,
            dano=dano,
            valor=valor,
            agilidade=0,
            tipo="arma",
            raridade=raridade
        )




    #============================= GERAR ANEL ===========================
    @classmethod
    def gerarAnel(cls, turno=5, raridade=None):

        qualidade = {
            "comum": 0.2,
            "raro": 0.3,
            "épico": 0.5,
            "lendário": 0.8,
            "mítico": 1.4
        }

        pesos = [70, 32, 9, 2, 0.3] #pesos = [70, 32, 9, 2, 0.5]
        if raridade == None:
            raridade = choices(list(qualidade.keys()),
                               weights=pesos,
                               k=1
                               )[0]
        agimin = 1
        dano = 0
        agimax = int(qualidade[raridade] * turno)
        match raridade:
            case "comum" :
                nomes = ["anel de plástico", "anel simples",
                         "anel de madeira", "anel enferrujado",
                         "anel de pedra"]
                nome = choice(nomes).title()
            case "raro":
                nomes = ["anel de prata", "anel de rubi", "anel do caçador",
                         "anel de ferro", "anel de safira"]
                nome = choice(nomes).title()
            case "épico":
                nomes = ["anel do trovão","anel do vento",
                         "anel das sombras","anel do vampiro",
                         "anel do assasino",
                         "anel do berseker"]
                nome = choice(nomes).title()
                agimin = int(agimax * 0.25)
                danomax = int(0.25 * agimax)
                if danomax < 1:
                    danomax = 1
                dano = random.randint(1, danomax)
            case "lendário":
                nomes = ["anel do dragão☯️","anel do imperador","anel de ouro",
                         "anel do titã","anel elementar☯️","anel do caçador"]
                nome = choice(nomes).title()
                danomax = int(0.3 * agimax)
                if danomax < 1 :
                    danomax = 1
                dano = random.randint(1,danomax)

                agimin = int(agimax * 0.55)
            case "mítico":
                nomes = ["anel do poder proibido☠️","anel divino✝️",
                         "anel do mago supremo♾️"]
                nome = choice(nomes).title()
                agimin = int(agimax * 0.85)
                danomax = int(0.5 * agimax)
                if danomax < 1:
                    danomax = 1
                danomin = int(0.3 * danomax)
                if danomin < 0 : danomin = 1
                dano = random.randint(danomin, danomax)
        if agimin <= 0 or agimax <= 0:
            agimin = 1
            agimax = 2
        agilidade = random.randint(agimin,agimax)
        valor = int(agilidade * 0.7)
        if valor <= 0: valor = 1
        tipo = "anel"
        return cls(
            nome=nome,
            dano=dano,
            valor=valor,
            agilidade=agilidade,
            tipo=tipo,
            raridade=raridade
        )



