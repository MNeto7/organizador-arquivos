#  funções auxiliares para mover e organizar os arquivos.
import json
import shutil # permite realizar operações de alto nível em arquivos e diretórios, como mover
from pathlib import Path
from config import EXTENSIONS_MAP
from datetime import datetime # permite manipular datas e horas

UNDO_LOG = Path("log_undo.json")

LOG_FILE = Path("log_organização.txt")

def get_category(file: Path) -> str:  # função que irá reconhecer as extensões dos arquivos
    for category, extensions in EXTENSIONS_MAP.items():
        if file.suffix.lower() in extensions:
            return category
    return "Outros"

def move_file(file: Path, destination_root: Path): # função que retorna se o arquivo foi movido com sucesso e para onde, ou se houve algum erro
    category = get_category(file)
    dest_folder = destination_root / category
    dest_folder.mkdir(exist_ok=True)

    destino = dest_folder / file.name
    try:
        shutil.move(str(file), str(destino))
        log_message = f"[{datetime.now()}] Movido: {file.name} -> {category}"
        print(log_message)
        append_to_log(log_message)
        save_undo_entry(original=str(file), destino=str(destino))
    except Exception as e:
        error_message = f"[{datetime.now}] Erro ao mover {file.name}: {e}"
        print(error_message)
        append_to_log(error_message)

def simulate_move(file: Path, destination_root: Path): # função usada para simular para qual destino o arquivo irá
    category = get_category(file)
    print(f"[Simulação] {file.name} seria movido para a paste: {category}.")

def append_to_log(message: str): # função que registra as mudanças no arquivo de log
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(message +"\n")

def undo_organize():
    if not UNDO_LOG.exists():
        print("❌ Nenhum histórico de organização encontrado.")
        return
    
    with open(UNDO_LOG, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in reversed(data):
        origem = Path(entry["original"])
        destino = Path(entry["destino"])
        try:
            if destino.exists():
                destino.rename(origem)
                print(f"↩️ Desfeito: {destino.name} voltou para {origem.parent}")
            else:
                print(f"⚠️ Arquivo não encontrado para desfazer: {destino}")
        except Exception as e:
            print(f"Erro ao desfazer {destino.name}: {e}")
    
    UNDO_LOG.unlink()

def save_undo_entry(original=str, destino=str): # função auxiliar para salvar o histórico de "desfazer"
    entry = {"original": original, "destino": destino}
    if UNDO_LOG.exists():
        with open(UNDO_LOG, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)

    with open(UNDO_LOG, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)