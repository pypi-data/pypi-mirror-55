from pathlib import Path
from shutil import copyfile


def extrair_exemplos():
    """Copia arquivos de exemplo de cálculo para o diretório corrente."""
    dir_exemplos = Path(__file__).parent

    for ext in ['*.ame', '*.ftl']:
        for i in dir_exemplos.glob(ext):
            copyfile(i, i.name)
