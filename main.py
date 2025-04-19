# ponto de entrada do programa
from pathlib import Path # permite trabalhar com caminhos de arquivos e diretórios
from config import SOURCE_FOLDER # importando do arquivo config
from utils import move_file, simulate_move, undo_organize # importando funções do arquivo utils
import argparse # O módulo argparse torna fácil a escrita de interfaces de linha de comando amigáveis
import schedule # permite agendar a execução de tarefas em horários específicos ou em intervalos
import time # permite trabalhar com datas e horas

def organize_folder(simular=False):  # função que irá simluar/ mover os arquivos
    for item in SOURCE_FOLDER.iterdir():
        if item.is_file():
            if simular:
                simulate_move(item, SOURCE_FOLDER)
            else:
                move_file(item, SOURCE_FOLDER)

if __name__ == "__main__":  # função principal
    parser = argparse.ArgumentParser(description="Organizador de Arquivos")
    parser.add_argument('--simular', action='store_true', help="Executa o modo simulação (não move o arquivo)")
    parser.add_argument('--loop', type=int, help="Executa continuamente a cada x minutos")
    parser.add_argument('--desfazer', action='store_true', help="Desfaz a última organização")
    args = parser.parse_args()
    
    if args.desfazer:
        undo_organize()
    elif args.loop:
        print(f"🔁 Modo contínuo ativado: organizando a cada {args.loop} minutos")
        schedule.every(args.loop).minutes.do(organize_folder, simular=args.simular)

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Execução interrompida pelo usuário.")
    else:
        organize_folder(simular=args.simular)