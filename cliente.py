"""Ponto de entrada do jogador: não importa o motor nem os sons."""

import argparse
from shutil import get_terminal_size

from rede.cliente_tcp import executar_cliente


def main():
    parser = argparse.ArgumentParser(description="Cliente LAN do RPG de terminal")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--nome", help="Nome do jogador, até 30 caracteres")
    parser.add_argument("--largura", type=int, default=min(160, max(40, get_terminal_size().columns)))
    args = parser.parse_args()
    if not 1 <= args.port <= 65535 or not 40 <= args.largura <= 160:
        parser.error("Porta ou largura (40–160 colunas) inválida.")
    nome = args.nome or input("Seu nome: ")
    try:
        executar_cliente(args.host, args.port, nome, args.largura)
    except (OSError, EOFError) as erro:
        parser.exit(1, f"Não foi possível continuar a conexão: {erro}\n")
    except KeyboardInterrupt:
        print("\nCliente encerrado.")


if __name__ == "__main__":
    main()
