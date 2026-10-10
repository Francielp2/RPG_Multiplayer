import io
import runpy
import sys
import unittest
from unittest.mock import MagicMock, patch

from rich.cells import cell_len
from rich.console import Console

# O som é substituído apenas neste processo de testes, sem abrir dispositivo.
_audio = patch.dict(sys.modules, {"som": MagicMock()})
_audio.start()
unittest.addModuleCleanup(_audio.stop)
from equipamento import Equipamento
from equipamento.pocao import Pocao
from jogador import Jogador
from loja import Loja
from partida import Partida
from interface import menu


class TestPocoes(unittest.TestCase):
    def setUp(self):
        self.jog = Jogador("Teste", 100)
        for alvo in ("jogador.jogador.mostrar_mensagem", "jogador.jogador.sleep",
                     "loja.loja.mostrar_mensagem", "loja.loja.sleep",
                     "partida.partida.mostrar_mensagem"):
            substituto = patch(alvo)
            substituto.start()
            self.addCleanup(substituto.stop)

    def usar(self, tipo, raridade="comum"):
        pocao = Pocao(tipo, raridade)
        self.jog.inventario.append(pocao)
        self.assertTrue(self.jog.usar_pocao(pocao))
        return pocao

    def test_raridades_duracoes_e_limites(self):
        for raridade, duracao in zip(Pocao.atributos, (1, 1, 2, 2, 3)):
            for tipo in Pocao.nomes:
                with self.subTest(raridade=raridade, tipo=tipo):
                    pocao = Pocao.gerarPocao(raridade, tipo)
                    self.assertEqual(pocao.duracao, 0 if tipo == "cura" else duracao)
                    self.assertGreaterEqual(pocao.valor, 4)
                    if tipo in ("forca", "agilidade"):
                        self.assertLessEqual(pocao.potencia, 3)
                    if tipo == "cura":
                        self.assertLessEqual(pocao.potencia, 20)
                    if tipo == "sorte":
                        self.assertLessEqual(pocao.potencia, .3)

    def test_cura_imediata_limitada_e_uma_por_rodada(self):
        self.jog.hp = 50
        self.usar("cura", "mítico")
        self.assertEqual(self.jog.hp, 70)
        self.assertEqual(self.jog.efeitos_pocoes, {})
        segunda = Pocao("cura")
        self.jog.inventario.append(segunda)
        self.assertFalse(self.jog.usar_pocao(segunda))
        self.assertIn(segunda, self.jog.inventario)
        self.jog.avancar_rodada_pocoes()
        self.assertEqual(self.jog.hp, 70)
        self.assertTrue(self.jog.usar_pocao(segunda))
        self.assertEqual(self.jog.hp, 75)

    def test_cura_nao_consumida_no_maximo_e_nao_reduz_hp_extra(self):
        pocao = Pocao("cura")
        self.jog.inventario.append(pocao)
        for hp in (100, 120):
            self.jog.hp = hp
            self.assertFalse(self.jog.usar_pocao(pocao))
            self.assertEqual(self.jog.hp, hp)
            self.assertIn(pocao, self.jog.inventario)
        self.jog.hp = 99
        self.assertTrue(self.jog.usar_pocao(pocao))
        self.assertEqual(self.jog.hp, 100)

    def test_bonus_entram_no_combate_e_expiram_sem_mudar_base(self):
        self.jog.danobonus = 2
        self.jog.agilidadebonus = 1
        self.jog.anel = Equipamento("Anel", dano=2, agilidade=3, tipo="anel")
        self.usar("forca", "épico")
        self.usar("agilidade", "épico")
        self.assertEqual(self.jog.dano, 6)
        self.assertEqual(self.jog.agilidade, 6)
        self.assertEqual(self.jog.danotot(5, 10), 11)
        self.assertEqual(self.jog.danotot(5, 20), 22)
        self.assertEqual(self.jog.agilidadetot(5), 11)
        self.jog.avancar_rodada_pocoes()
        self.assertEqual(self.jog.dano, 6)
        self.jog.avancar_rodada_pocoes()
        self.assertEqual((self.jog.dano, self.jog.agilidade), (4, 4))
        self.assertEqual((self.jog.danobonus, self.jog.agilidadebonus), (2, 1))

    def test_sorte_limitada_sem_perder_ganhos_permanentes(self):
        self.jog.sorte = 1.8
        self.usar("sorte", "mítico")
        self.assertEqual(self.jog.sorte_total, 2.0)
        with patch("jogador.jogador.randint", return_value=70):
            self.assertTrue(self.jog.roletar_sorte(35))
        self.jog.aumentar_sorte()
        for _ in range(3):
            self.jog.avancar_rodada_pocoes()
        self.assertEqual(self.jog.sorte, 1.9)
        self.assertEqual(self.jog.sorte_total, 1.9)
        with patch("jogador.jogador.randint", return_value=70):
            self.assertFalse(self.jog.roletar_sorte(35))
        self.jog.sorte = 2.0
        outra = Pocao("sorte")
        self.jog.inventario.append(outra)
        self.assertFalse(self.jog.usar_pocao(outra))
        self.assertIn(outra, self.jog.inventario)

    def test_nao_acumula_nao_reequipa_e_nao_reutiliza(self):
        usada = self.usar("forca")
        outra = Pocao("forca", "mítico")
        self.jog.inventario.append(outra)
        self.assertFalse(self.jog.usar_pocao(outra))
        self.assertFalse(self.jog.usar_pocao(usada))
        self.assertEqual(self.jog.bonus_pocao("forca"), 1)
        self.jog.equipar(outra)
        self.assertIsNone(self.jog.arma)
        self.assertEqual(len(self.jog.inventario), 1)
        self.assertTrue(self.jog.vender(outra))
        self.assertEqual(self.jog.moedas, 4)
        self.assertEqual(self.jog.bonus_pocao("forca"), 1)

    def test_morto_nao_usa_pocao(self):
        self.jog.hp = 0
        pocao = Pocao("cura")
        self.jog.inventario.append(pocao)
        self.assertFalse(self.jog.usar_pocao(pocao))
        self.assertIn(pocao, self.jog.inventario)

    def test_compra_estoque_compartilhado_e_venda(self):
        loja = Loja()
        pocao = Pocao("forca")
        loja.estoque = [pocao]
        self.jog.moedas = 10
        with patch("builtins.input", return_value="0"):
            loja.compra(self.jog)
        self.assertEqual(loja.estoque, [])
        self.assertEqual(self.jog.moedas, 6)
        self.assertIn(pocao, self.jog.inventario)
        self.assertTrue(self.jog.vender(pocao))
        self.assertEqual(self.jog.moedas, 7)

    def test_geracao_e_renovacao_da_loja(self):
        loja = Loja()
        for chance, tipo in ((.50, "arma"), (.51, "anel"), (.765, "armadura"), (.85, "pocao")):
            with patch("loja.loja.random", return_value=chance):
                loja.novo_equip()
            self.assertEqual(loja.estoque[-1].tipo, tipo)
        loja.turno = 10000
        with patch("loja.loja.random", return_value=.9):
            loja.att_loja()
        self.assertEqual(len(loja.estoque), loja.slot)
        self.assertTrue(all(isinstance(item, Pocao) for item in loja.estoque))

    def test_inventario_usa_ou_vende_pocao(self):
        self.jog.inventario = [Pocao("forca")]
        with patch("builtins.input", side_effect=["0", "0"]), patch("jogador.jogador.print"):
            self.jog.mostrar_inventario()
        self.assertEqual(self.jog.inventario, [])
        self.assertEqual(self.jog.bonus_pocao("forca"), 1)
        self.jog.inventario = [Pocao("cura")]
        with patch("builtins.input", side_effect=["0", "1"]), patch("jogador.jogador.print"):
            self.jog.mostrar_inventario()
        self.assertEqual(self.jog.inventario, [])
        self.assertEqual(self.jog.moedas, 1)

    def test_esc_volta_sem_comprar_vender_ou_atacar(self):
        from combate import Combate

        pocao = Pocao("forca")
        self.jog.inventario = [pocao]
        loja = Loja()
        loja.estoque = [pocao]
        self.jog.moedas = 10
        with patch("loja.loja.ler_opcao", return_value=None):
            self.assertIsNone(loja.compra(self.jog))
        with patch("partida.partida.ler_opcao", side_effect=["0", None, None]), \
                patch("jogador.jogador.print"):
            self.jog.mostrar_inventario()
        combate = Combate(self.jog, [self.jog, Jogador("B", 100), Jogador("C", 100)], 0)
        with patch("combate.combate.ler_opcao", return_value=None), patch("combate.combate.print"):
            self.assertFalse(combate.escolher_alvo())
        self.assertEqual(self.jog.moedas, 10)
        self.assertEqual(self.jog.inventario, [pocao])
        self.assertEqual(loja.estoque, [pocao])
        self.assertEqual(self.jog.efeitos_pocoes, {})

    def test_tabelas_mostram_pocoes_e_rodadas(self):
        loja = Loja()
        loja.estoque = [Pocao(tipo, "épico") for tipo in Pocao.nomes]
        self.usar("forca", "épico")
        for largura in (40, 80, 120):
            saida = io.StringIO()
            console = Console(file=saida, width=largura, color_system=None)
            with patch("loja.loja.print", console.print), patch.object(menu, "print", console.print):
                loja.mostrar_loja(self.jog)
                menu.Tabelajogadores([self.jog], self.jog)
                menu.mostrar_acoes(self.jog, 1)
            texto = saida.getvalue()
            self.assertIn("POÇÕES", texto)
            if largura >= 80:
                self.assertIn("Imediata", texto)
            self.assertIn("2 rodada(s)", texto)
            self.assertTrue(all(cell_len(linha) <= largura for linha in texto.splitlines()))

    def test_ciclo_principal_so_desconta_ao_encerrar_rodada(self):
        self.usar("forca", "épico")
        outro = Jogador("Outro", 100)
        partida = Partida([self.jog, outro])
        telas = []
        ataques = iter((False, True, True))

        class EncerrarEnsaio(Exception):
            pass

        def tela(jogadores, jogatual):
            telas.append(jogatual)
            if len(telas) == 4:
                raise EncerrarEnsaio()

        with patch("builtins.input", return_value="2"), \
                patch.object(Partida, "registrar_jogadores", return_value=partida.jogadores), \
                patch.object(Partida, "validar_opc", return_value=1), \
                patch.object(Partida, "ganhar_moeda"), \
                patch("interface.funcoes.limpar_tela"), \
                patch("interface.menu.Tabelajogadores", side_effect=tela), \
                patch("interface.menu.mostrar_acoes"), \
                patch("combate.Combate", return_value=MagicMock(atacar=lambda: next(ataques))), \
                patch("eventos.EventoAleatorio", return_value=MagicMock()), \
                patch("loja.Loja", return_value=MagicMock()):
            with self.assertRaises(EncerrarEnsaio):
                runpy.run_path("main.py", run_name="__main__")
        self.assertEqual(telas, [self.jog, self.jog, outro, self.jog])
        self.assertEqual(self.jog.efeitos_pocoes["forca"]["rodadas"], 1)


if __name__ == "__main__":
    unittest.main()
