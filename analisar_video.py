#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Analisador de Vídeos')
    parser.add_argument('--arquivo', required=True, help='Caminho para o arquivo de vídeo')
    parser.add_argument('--jogo', default='rocket_league', choices=['rocket_league', 'rainbow_six'], 
                        help='Tipo de jogo (rocket_league ou rainbow_six)')
    parser.add_argument('--saida', default='data/results', help='Diretório para salvar resultados')
    args = parser.parse_args()
    
    print(f"Iniciando análise do vídeo: {args.arquivo}")
    print(f"Tipo de jogo: {args.jogo}")
    print(f"Diretório de saída dos resultados: {args.saida}")

    # Identifica o executável do Python no ambiente virtual
    if sys.platform == 'win32':
        python_exec = os.path.join('venv', 'Scripts', 'python.exe')
    else:
        python_exec = os.path.join('venv', 'bin', 'python')

    if not os.path.isfile(python_exec):
        print(f"Erro: Não foi encontrado o Python do ambiente virtual em: {python_exec}")
        print("Certifique-se de que o ambiente virtual foi criado (venv) e instalado corretamente.")
        sys.exit(1)

    cmd = f'"{python_exec}" video_analysis/gameplay_video_processor.py --video "{args.arquivo}" --game "{args.jogo}" --output "{args.saida}"'
    print(f"Executando comando: {cmd}")
    exit_code = os.system(cmd)
    
    if exit_code == 0:
        print("Processamento concluído com sucesso!")
    else:
        print(f"Ocorreu um erro ao processar o vídeo. Código de saída: {exit_code}")

if __name__ == '__main__':
    main()