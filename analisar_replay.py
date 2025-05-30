#!/usr/bin/env python3
import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Analisador de Replays')
    parser.add_argument('--arquivo', required=True, help='Caminho para o arquivo de replay')
    parser.add_argument('--jogo', default='rocket_league', choices=['rocket_league', 'rainbow_six'], 
                        help='Tipo de jogo (rocket_league ou rainbow_six)')
    parser.add_argument('--saida', default='data/results', help='Diretório para salvar resultados')
    args = parser.parse_args()
    
    # Ativar ambiente virtual
    if sys.platform == 'win32':
        activate_script = os.path.join('venv', 'Scripts', 'activate')
        os.system(f'call {activate_script} && python integrador.py --replay {args.arquivo} --game {args.jogo} --output {args.saida}')
    else:
        activate_script = os.path.join('venv', 'bin', 'activate')
        os.system(f'source {activate_script} && python integrador.py --replay {args.arquivo} --game {args.jogo} --output {args.saida}')

if __name__ == '__main__':
    main()
