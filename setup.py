 #!/usr/bin/env python3
"""
Script de configuração para a IA de Análise de Replays.
Este script instala todas as dependências necessárias e configura o ambiente.
"""

import os
import sys
import subprocess
import platform

def print_header(message):
    """Imprime cabeçalho formatado."""
    print("\n" + "=" * 60)
    print(f" {message}")
    print("=" * 60)

def check_python_version():
    """Verifica se a versão do Python é compatível."""
    print_header("Verificando versão do Python")
    
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 8):
        print(f"[ERRO] Python 3.8 ou superior é necessário. Versão atual: {major}.{minor}")
        print("Por favor, instale uma versão mais recente do Python.")
        return False
    
    print(f"[OK] Versão do Python: {major}.{minor}")
    return True

def create_virtual_environment():
    """Cria um ambiente virtual Python."""
    print_header("Configurando ambiente virtual")
    
    if os.path.exists("venv"):
        print("[INFO] Ambiente virtual já existe.")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("[OK] Ambiente virtual criado com sucesso.")
        return True
    except subprocess.CalledProcessError:
        print("[ERRO] Falha ao criar ambiente virtual.")
        return False

def install_dependencies():
    """Instala as dependências necessárias."""
    print_header("Instalando dependências")
    
    # Determinar o caminho do pip no ambiente virtual
    if platform.system() == "Windows":
        pip_path = os.path.join("venv", "Scripts", "pip")
    else:
        pip_path = os.path.join("venv", "bin", "pip")
    
    # Atualizar pip
    try:
        subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
        print("[OK] Pip atualizado.")
    except subprocess.CalledProcessError:
        print("[AVISO] Falha ao atualizar pip, continuando com a versão atual.")
    
    # Instalar dependências
    requirements = [
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "flask",
        "opencv-python",
        "requests",
        "tqdm"
    ]
    
    for package in requirements:
        try:
            print(f"Instalando {package}...")
            subprocess.run([pip_path, "install", package], check=True)
            print(f"[OK] {package} instalado.")
        except subprocess.CalledProcessError:
            print(f"[ERRO] Falha ao instalar {package}.")
            return False
    
    print("[OK] Todas as dependências foram instaladas.")
    return True

def check_ffmpeg():
    """Verifica se o FFmpeg está instalado (opcional)."""
    print_header("Verificando FFmpeg (opcional)")
    
    try:
        result = subprocess.run(["ffmpeg", "-version"], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               text=True)
        if result.returncode == 0:
            print("[OK] FFmpeg está instalado.")
            return True
    except FileNotFoundError:
        pass
    
    print("[AVISO] FFmpeg não encontrado. A análise de vídeo não estará disponível.")
    print("Para instalar o FFmpeg:")
    if platform.system() == "Windows":
        print("  1. Baixe em: https://ffmpeg.org/download.html")
        print("  2. Adicione ao PATH do sistema")
    elif platform.system() == "Darwin":  # macOS
        print("  Execute: brew install ffmpeg")
    else:  # Linux
        print("  Execute: sudo apt-get install ffmpeg")
    
    return False

def create_directories():
    """Cria diretórios necessários para o funcionamento."""
    print_header("Criando diretórios")
    
    directories = [
        "data/uploads",
        "data/results",
        "data/temp"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"[OK] Diretório criado: {directory}")
    
    return True

def create_wrapper_scripts():
    """Cria scripts de wrapper para facilitar o uso."""
    print_header("Criando scripts de execução")
    
    # Script para análise de replay
    with open("analisar_replay.py", "w") as f:
        f.write("""#!/usr/bin/env python3
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
""")
    
    # Script para análise de vídeo
    with open("analisar_video.py", "w") as f:
        f.write("""#!/usr/bin/env python3
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
    
    # Ativar ambiente virtual
    if sys.platform == 'win32':
        activate_script = os.path.join('venv', 'Scripts', 'activate')
        os.system(f'call {activate_script} && python video_analysis/gameplay_video_processor.py --video {args.arquivo} --game {args.jogo} --output {args.saida}')
    else:
        activate_script = os.path.join('venv', 'bin', 'activate')
        os.system(f'source {activate_script} && python video_analysis/gameplay_video_processor.py --video {args.arquivo} --game {args.jogo} --output {args.saida}')

if __name__ == '__main__':
    main()
""")
    
    # Script para iniciar interface web
    with open("iniciar_interface.py", "w") as f:
        f.write("""#!/usr/bin/env python3
import os
import sys

def main():
    # Ativar ambiente virtual
    if sys.platform == 'win32':
        activate_script = os.path.join('venv', 'Scripts', 'activate')
        os.system(f'call {activate_script} && python interface/app.py')
    else:
        activate_script = os.path.join('venv', 'bin', 'activate')
        os.system(f'source {activate_script} && python interface/app.py')

if __name__ == '__main__':
    main()
""")
    
    # Tornar scripts executáveis em sistemas Unix
    if platform.system() != "Windows":
        os.chmod("analisar_replay.py", 0o755)
        os.chmod("analisar_video.py", 0o755)
        os.chmod("iniciar_interface.py", 0o755)
    
    print("[OK] Scripts de execução criados.")
    return True

def main():
    """Função principal de configuração."""
    print_header("Configuração da IA de Análise de Replays")
    
    # Verificar requisitos
    if not check_python_version():
        return False
    
    # Configurar ambiente
    if not create_virtual_environment():
        return False
    
    if not install_dependencies():
        return False
    
    check_ffmpeg()  # Opcional
    
    if not create_directories():
        return False
    
    if not create_wrapper_scripts():
        return False
    
    print_header("Configuração concluída com sucesso!")
    print("\nPara analisar um replay:")
    print("  python analisar_replay.py --arquivo caminho/para/seu/replay.replay")
    print("\nPara iniciar a interface web:")
    print("  python iniciar_interface.py")
    print("\nPara analisar um vídeo (requer FFmpeg):")
    print("  python analisar_video.py --arquivo caminho/para/seu/video.mp4")
    
    return True

if __name__ == "__main__":
    main()
