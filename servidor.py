"""Ponto de entrada da sala LAN. O servidor não abre áudio nem pede input."""

import argparse
import os
from math import isfinite

from rede.servidor_tcp import Servidor


def main():
    parser = argparse.ArgumentParser(description="Servidor LAN do RPG de terminal")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--jogadores", type=int, default=2)
    parser.add_argument("--timeout", type=float, default=120, help="Segundos para entrada no lobby ou resposta")
    parser.add_argument("--hp", type=int, default=100, help="HP inicial; use 20 para um ensaio rápido")
    parser.add_argument("--sem-pausas", action="store_true", help="Remove animações de espera para testes")
    args = parser.parse_args()
    if (not 0 <= args.port <= 65535 or not 2 <= args.jogadores <= 16
            or not isfinite(args.timeout) or args.timeout <= 0 or args.hp <= 0):
        parser.error("Porta, quantidade (2–16), timeout ou HP inválidos.")
    os.environ["RPG_SEM_SOM"] = "1"
    servidor = Servidor(args.host, args.port, args.jogadores, args.timeout, args.hp,
                        fator_pausa=0 if args.sem_pausas else 1)
    try:
        servidor.rodar()
    except OSError as erro:
        parser.exit(1, f"Não foi possível abrir o servidor: {erro}\n")


if __name__ == "__main__":
    main()
