# configurações
from pathlib import Path

# Caminho da pasta que será organizada
SOURCE_FOLDER = Path.home() / "Downloads" # Você pode mudar o diretório dependendo da pasta que quer organizar

# Extensões de arquivo e pastas de destino
EXTENSIONS_MAP = {
    "Imagens": [".jpg", ".jpeg", "png", ".gif", ".bmp"],
    "Documentos": [".pdf", "docx", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Música": [".mp3", ".wav", ".ogg"],
    "Instaladores": [".msi", ".exe", ".deb"],
    "Compactados": ['.zip', '.rar', '.7z', '.tar'],
    "Outros": [] # Arquivos que não se encaixam nos anteriores
}