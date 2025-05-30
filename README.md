# Guia Rápido - IA de Análise de Replays

Este pacote contém uma IA completa para análise de replays e vídeos de Rocket League e Rainbow Six Siege.

## Requisitos

- Python 3.8 ou superior
- Bibliotecas Python (instaladas automaticamente pelo script de configuração)
- FFmpeg (opcional, para análise de vídeo)

## Instalação Rápida

1. Extraia o arquivo zip em qualquer pasta
2. Execute o script de instalação:

```bash
python setup.py
```

## Uso Rápido

### Para analisar um replay:

```bash
python analisar_replay.py --arquivo caminho/para/seu/replay.replay
```

### Para iniciar a interface web:

```bash
python iniciar_interface.py
```
Depois acesse http://localhost:5000 no navegador

### Para analisar um vídeo:

```bash
python analisar_video.py --arquivo caminho/para/seu/video.mp4
```

## Estrutura do Pacote

- `analisar_replay.py`: Script principal para análise de replays
- `analisar_video.py`: Script principal para análise de vídeos
- `iniciar_interface.py`: Inicia a interface web
- `setup.py`: Configura o ambiente e instala dependências
- `parser/`: Módulos para processamento de arquivos de replay
- `modelo/`: Algoritmos de análise
- `visualizacao/`: Geração de gráficos e visualizações
- `video_analysis/`: Processamento de vídeos
- `interface/`: Interface web
- `data/`: Pasta para armazenar dados e resultados

## Solução de Problemas

- **Erro ao analisar vídeo**: Instale o FFmpeg com `sudo apt-get install ffmpeg`
- **Interface web não inicia**: Verifique se a porta 5000 está disponível
- **Erro de dependências**: Execute novamente `python setup.py`

Para mais informações, consulte a documentação completa em `docs/manual_completo.md`.
