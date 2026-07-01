from core.restore.dbRestoreStrategy import DBRestoreStrategy
from core.decompress import decompressHandler
import shutil
from pathlib import Path

class SQLiteStrategy(DBRestoreStrategy):
    def restore(self, host: str, port: int, user: str, password: str, database: str, backup_file: str) -> bool:
        """
        Realiza el proceso de restauración para SQLite.
        Esto reemplaza el archivo de la base de datos actual con el del backup.
        """
        db_path = Path(database)
        backup_path = Path(backup_file)

        print(f"Descomprimiendo {backup_path} a {db_path}...")
        
        decompressHandler(backup_path, db_path)
        
        return True