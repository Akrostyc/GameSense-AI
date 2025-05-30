
"""

Módulo principal para integração de todos os componentes do analisador de replays.
Este script integra parser, análise e visualização em um fluxo completo.
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar componentes
from parser.rocket_league_parser import RocketLeagueParser, create_sample_replay
from modelo.rocket_league_analyzer import RocketLeagueAnalyzer
from visualizacao.rocket_league_visualizer import RocketLeagueVisualizer

class ReplayAnalyzerIntegrator:
    """
    Integrador para o sistema de análise de replays.
    
    Esta classe coordena o fluxo completo de processamento de replays,
    desde o parsing até a visualização dos resultados.
    """
    
    def __init__(self, data_dir=None):
        """
        Inicializa o integrador.
        
        Args:
            data_dir (str, optional): Diretório para armazenar dados e resultados
        """
        # Definir diretórios
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        if data_dir:
            self.data_dir = data_dir
        else:
            self.data_dir = os.path.join(self.base_dir, 'data')
        
        # Criar subdiretórios
        self.uploads_dir = os.path.join(self.data_dir, 'uploads')
        self.results_dir = os.path.join(self.data_dir, 'results')
        self.visualizations_dir = os.path.join(self.data_dir, 'visualizations')
        
        os.makedirs(self.uploads_dir, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.visualizations_dir, exist_ok=True)
        
        # Inicializar componentes
        self.parser = None
        self.analyzer = RocketLeagueAnalyzer()
        self.visualizer = RocketLeagueVisualizer(self.visualizations_dir)
    
    def process_replay(self, replay_path, result_id=None):
        """
        Processa um arquivo de replay completo.
        
        Args:
            replay_path (str): Caminho para o arquivo de replay
            result_id (str, optional): ID para os resultados
            
        Returns:
            dict: Resultados do processamento ou None em caso de falha
        """
        # Verificar se o arquivo existe
        if not os.path.exists(replay_path):
            print(f"Erro: Arquivo {replay_path} não encontrado.")
            return None
        
        # Gerar ID de resultado se não fornecido
        if not result_id:
            result_id = os.path.basename(replay_path).replace('.replay', '') + '_' + datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Criar diretório para os resultados
        result_dir = os.path.join(self.results_dir, result_id)
        os.makedirs(result_dir, exist_ok=True)
        
        # Configurar visualizador para salvar no diretório de resultados
        self.visualizer.set_output_dir(result_dir)
        
        # Etapa 1: Parsing do replay
        print(f"Analisando replay: {replay_path}")
        self.parser = RocketLeagueParser(replay_path)
        
        if not self.parser.parse():
            print("Falha ao analisar o replay.")
            return None
        
        # Salvar dados do replay
        replay_data_path = os.path.join(result_dir, 'replay_data.json')
        self.parser.export_to_json(replay_data_path)
        
        # Obter DataFrames
        player_df = self.parser.get_player_positions_dataframe()
        ball_df = self.parser.get_ball_positions_dataframe()
        
        # Salvar DataFrames para referência
        player_df.to_csv(os.path.join(result_dir, 'player_positions.csv'), index=False)
        ball_df.to_csv(os.path.join(result_dir, 'ball_positions.csv'), index=False)
        
        # Etapa 2: Análise do replay
        print("Realizando análise avançada...")
        # Preparar dados para o analisador no formato esperado
        replay_data = {
            'metadata': self.parser.get_metadata(),
            'players': self.parser.get_players(),
            'events': self.parser.get_events()
        }
        self.analyzer.load_data(replay_data)
        self.analyzer.load_dataframes(player_df, ball_df)
        self.analyzer.analyze()
        
        # Obter resultados da análise
        analysis_results = self.analyzer.analysis_results
        overall_score = self.analyzer.get_overall_score()
        findings = self.analyzer.get_key_findings()
        recommendations = self.analyzer.get_recommendations()
        
        # Salvar resultados da análise
        with open(os.path.join(result_dir, 'analysis_results.json'), 'w') as f:
            json.dump({
                'analysis': analysis_results,
                'overall_score': overall_score,
                'findings': findings,
                'recommendations': recommendations
            }, f, indent=2)
        
        # Etapa 3: Gerar visualizações
        print("Gerando visualizações...")
        
        # Visualizações básicas
        self.visualizer.create_heatmap(player_df, save_as='heatmap.png')
        self.visualizer.create_ball_trajectory(ball_df, save_as='ball_trajectory.png')
        self.visualizer.create_boost_usage_chart(player_df, self.parser.get_players(), save_as='boost_usage.png')
        self.visualizer.create_speed_chart(player_df, self.parser.get_players(), save_as='speed.png')
        self.visualizer.create_distance_to_ball_chart(player_df, ball_df, self.parser.get_players(), save_as='distance_to_ball.png')
        self.visualizer.create_team_spread_chart(player_df, self.parser.get_players(), save_as='team_spread.png')
        self.visualizer.create_analysis_radar_chart(analysis_results, save_as='analysis_radar.png')
        self.visualizer.create_event_timeline(self.parser.get_events(), save_as='event_timeline.png')
        
        # Compilar resultados
        results = {
            'id': result_id,
            'replay_path': replay_path,
            'result_dir': result_dir,
            'metadata': self.parser.get_metadata(),
            'players': self.parser.get_players(),
            'events': self.parser.get_events(),
            'analysis': analysis_results,
            'overall_score': overall_score,
            'findings': findings,
            'recommendations': recommendations,
            'visualizations': {
                'heatmap': os.path.join(result_dir, 'heatmap.png'),
                'ball_trajectory': os.path.join(result_dir, 'ball_trajectory.png'),
                'boost_usage': os.path.join(result_dir, 'boost_usage.png'),
                'speed': os.path.join(result_dir, 'speed.png'),
                'distance_to_ball': os.path.join(result_dir, 'distance_to_ball.png'),
                'team_spread': os.path.join(result_dir, 'team_spread.png'),
                'analysis_radar': os.path.join(result_dir, 'analysis_radar.png'),
                'event_timeline': os.path.join(result_dir, 'event_timeline.png')
            }
        }
        
        print(f"Processamento concluído. Resultados salvos em: {result_dir}")
        return results
    
    def create_and_process_demo_replay(self):
        """
        Cria e processa um replay de demonstração.
        
        Returns:
            dict: Resultados do processamento ou None em caso de falha
        """
        # Criar um replay de exemplo
        sample_replay = create_sample_replay(self.uploads_dir)
        
        # Processar o replay
        return self.process_replay(sample_replay, 'demo_replay')
    
    def get_result_summary(self, result_id):
        """
        Obtém um resumo dos resultados de uma análise.
        
        Args:
            result_id (str): ID dos resultados
            
        Returns:
            dict: Resumo dos resultados ou None se não encontrado
        """
        result_dir = os.path.join(self.results_dir, result_id)
        
        if not os.path.exists(result_dir):
            print(f"Erro: Resultados com ID {result_id} não encontrados.")
            return None
        
        # Carregar resultados da análise
        analysis_path = os.path.join(result_dir, 'analysis_results.json')
        
        if not os.path.exists(analysis_path):
            print(f"Erro: Arquivo de análise não encontrado em {result_dir}.")
            return None
        
        with open(analysis_path, 'r') as f:
            analysis_data = json.load(f)
        
        # Carregar dados do replay
        replay_data_path = os.path.join(result_dir, 'replay_data.json')
        
        if not os.path.exists(replay_data_path):
            print(f"Erro: Arquivo de dados do replay não encontrado em {result_dir}.")
            return None
        
        with open(replay_data_path, 'r') as f:
            replay_data = json.load(f)
        
        # Compilar resumo
        summary = {
            'id': result_id,
            'metadata': replay_data.get('metadata', {}),
            'players': replay_data.get('players', []),
            'events': replay_data.get('events', []),
            'overall_score': analysis_data.get('overall_score', {}),
            'findings': analysis_data.get('findings', []),
            'recommendations': analysis_data.get('recommendations', {}),
            'visualizations': {
                'heatmap': os.path.join(result_dir, 'heatmap.png'),
                'ball_trajectory': os.path.join(result_dir, 'ball_trajectory.png'),
                'boost_usage': os.path.join(result_dir, 'boost_usage.png'),
                'speed': os.path.join(result_dir, 'speed.png'),
                'distance_to_ball': os.path.join(result_dir, 'distance_to_ball.png'),
                'team_spread': os.path.join(result_dir, 'team_spread.png'),
                'analysis_radar': os.path.join(result_dir, 'analysis_radar.png'),
                'event_timeline': os.path.join(result_dir, 'event_timeline.png')
            }
        }
        
        return summary


# Função principal para uso via linha de comando
def main():
    parser = argparse.ArgumentParser(description='Analisador de Replays de Rocket League')
    parser.add_argument('--replay', type=str, help='Caminho para o arquivo de replay')
    parser.add_argument('--demo', action='store_true', help='Usar replay de demonstração')
    parser.add_argument('--result-id', type=str, help='ID para os resultados')
    parser.add_argument('--data-dir', type=str, help='Diretório para armazenar dados e resultados')
    
    args = parser.parse_args()
    
    # Inicializar integrador
    integrator = ReplayAnalyzerIntegrator(args.data_dir)
    
    # Processar replay
    if args.demo:
        results = integrator.create_and_process_demo_replay()
    elif args.replay:
        results = integrator.process_replay(args.replay, args.result_id)
    else:
        parser.print_help()
        return
    
    if results:
        print("\nResumo dos Resultados:")
        print(f"ID: {results['id']}")
        print(f"Mapa: {results['metadata'].get('map_name', 'Desconhecido')}")
        print(f"Tipo de Partida: {results['metadata'].get('match_type', 'Desconhecido')}")
        print(f"Duração: {results['metadata'].get('duration', 0)} segundos")
        print(f"Jogadores: {len(results['players'])}")
        print(f"Eventos: {len(results['events'])}")
        print(f"Pontuação Geral: {results['overall_score']['overall_score']}/100")
        
        print("\nPontuações por Categoria:")
        for category, score in results['overall_score']['category_scores'].items():
            print(f"  {category}: {score}/100")
        
        print("\nPrincipais Insights:")
        for finding in results['findings'][:5]:  # Mostrar apenas os 5 primeiros
            print(f"- {finding}")
        
        print("\nVisualizações geradas:")
        for name, path in results['visualizations'].items():
            print(f"- {name}: {path}")


if __name__ == "__main__":
    main()
