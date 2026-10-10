"""Uma única sequência de regras, reutilizada no jogo local e no servidor."""

from interface import io


def executar_partida(jogadores):
    import som
    from combate import Combate
    from eventos import EventoAleatorio
    from interface.funcoes import limpar_tela
    from interface.menu import mostrar_acoes, Tabelajogadores
    from loja import Loja
    from partida import Partida

    partida = Partida(jogadores)
    loja = Loja()
    jogatual = 0
    turno = rodada = 1
    while True:
        partida.verificar_mortos()
        if partida.fim_partida():
            return partida
        jog = jogadores[jogatual]
        io.atualizar_estado(jogadores, jog, turno, rodada)
        limpar_tela()
        evento = EventoAleatorio(turno=turno, jogadores=jogadores)
        Tabelajogadores(jogadores=jogadores, jogatual=jog)
        mostrar_acoes(jog, turno=turno)
        loja.turno = turno
        opc = Partida.validar_opc([1, 2, 3, 4], "Sua opção:")

        if opc == 1:
            ordem_turno = jogadores.copy()
            som.atacar.play()
            combate = Combate(jog=jog, jogadores=jogadores, indice=jogatual)
            if combate.atacar():
                partida.verificar_mortos()
                if partida.fim_partida():
                    return partida
                Partida.ganhar_moeda(rodada=rodada, jog=jog)
                evento.executar()
                partida.verificar_mortos()
                if partida.fim_partida():
                    return partida
                proximo, fim_rodada = partida.proximo_jogador(jog, ordem_turno)
                jogatual = jogadores.index(proximo)
                if fim_rodada:
                    partida.encerrar_rodada()
                    loja.chance_att_loja()
                    rodada += 1
                turno += 1
        elif opc == 2:
            io.anunciar(f"{jog.nome} abriu a loja compartilhada.")
            loja.entrar_loja(jog=jog)
        elif opc == 3:
            io.anunciar(f"{jog.nome} abriu seu inventário.")
            with io.privado(jog):
                jog.mostrar_inventario()
