from core.restore.dbRestoreStrategy import DBRestoreStrategy
import os
import subprocess
from core.decompress import decompressHandler
import shutil
from pathlib import Path

class PostgreSQLStrategy(DBRestoreStrategy):
    def restore(self, host: str, port: int, user: str, password: str, database: str, backup_file: str) -> bool:
        """
        Realiza el proceso de restauración para PostgreSQL desde un archivo .gz.
        """
        backup_path = Path(backup_file)
        sql_file_path = backup_path.with_suffix('') # backup.sql

        decompressHandler(backup_path, sql_file_path)

        # 2. Ejecutar psql para restaurar
        env = os.environ.copy()
        env["PGPASSWORD"] = password
        
        comando = [
            "psql",
            "-h", host,
            "-p", str(port),
            "-U", user,
            "-d", database,
            "-f", str(sql_file_path)
        ]

        print(f"\nRestaurando base de datos PostgreSQL '{database}'...")
        subprocess.run(comando, env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.remove(sql_file_path)
        return True