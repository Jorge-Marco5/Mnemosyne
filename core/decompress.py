import gzip
import shutil
import os
from pathlib import Path

def decompressHandler(file_gz: Path, final_path: Path):
    print("\nDescomprimiendo archivo de respaldo...")
    with gzip.open(file_gz, 'rb') as f_input:
        with open(final_path, 'wb') as f_output:
            shutil.copyfileobj(f_input, f_output)
    # Eliminar el archivo .gz temporal
    os.remove(file_gz)
    # Tamaño del archivo en bytes
    return final_path