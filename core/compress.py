import gzip
import shutil
import os
from pathlib import Path

def compressHandler(file_sql: Path, final_path: Path):
    print("\nComprimiendo archivo de respaldo...")
    with open(file_sql, 'rb') as f_input:
        with gzip.open(final_path, 'wb') as f_output:
            shutil.copyfileobj(f_input, f_output)
            
    os.remove(file_sql)
    return final_path