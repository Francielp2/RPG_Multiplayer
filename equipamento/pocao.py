"""Consumíveis com bônus pequenos, sem crescimento ilimitado por turno."""

from random import choice, choices

from equipamento import Equipamento


class Pocao(Equipamento):
    # Duração dos bônus, preço, cura imediata, agilidade, força e sorte.
    atributos = {
        "comum": (1, 4, 5, 1, 1, 0.1),
        "raro": (1, 6, 8, 2, 2, 0.1),
        "épico": (2, 9, 12, 2, 2, 0.2),
        "lendário": (2, 12, 16, 3, 3, 0.2),
        "mítico": (3, 18, 20, 3, 3, 0.3),
    }
    nomes = {"cura": "Cura", "agilidade": "Agilidade", "forca": "Força", "sorte": "Sorte"}

    def __init__(self, efeito, raridade="comum"):
        duracao, valor, *bonus = self.atributos[raridade]
        self.efeito = efeito
        self.duracao = 0 if efeito == "cura" else duracao
        self.potencia = dict(zip(self.nomes, bonus))[efeito]
        super().__init__(nome=f"Poção de {self.nomes[efeito]}", valor=valor,
                         tipo="pocao", raridade=raridade)

    @property
    def descricao_efeito(self):
        if self.efeito == "cura":
            return f"+{self.potencia} HP"
        if self.efeito == "sorte":
            return f"+{self.potencia:.1f}x sorte"
        return f"+{self.potencia} {self.nomes[self.efeito].lower()}"

    @property
    def descricao_duracao(self):
        return "Imediata" if self.efeito == "cura" else f"{self.duracao} rodada(s)"

    @classmethod
    def gerarPocao(cls, raridade=None, efeito=None):
        if raridade is None:
            raridade = choices(list(cls.atributos), weights=[70, 32, 9, 2, 0.4], k=1)[0]
        if efeito is None:
            efeito = choice(list(cls.nomes))
        return cls(efeito, raridade)
