import gzip
import shutil
import os
from pathlib import Path

def compressHandler(file_sql: Path, final_path: Path):
    print("\nComprimiendo archivo de respaldo...")
    with open(file_sql, 'rb') as f_input:
        with gzip.open(final_path, 'wb') as f_output:
            shutil.copyfileobj(f_input, f_output)
            
    # Eliminar el archivo SQL temporal sin comprimir
    os.remove(file_sql)
    # Tamaño del archivo en bytes
    
    return final_path