from core.backups.dbBackupStrategy import DBBackupStrategy
import os
import sqlite3
import shutil
from pathlib import Path
from datetime import datetime
from core.compress import compressHandler
from core.data_service import DataService

historyHandler = DataService()

class SQLiteStrategy(DBBackupStrategy):
    backup_path = os.getenv("BACKUPS_PATH")
    path_base = Path(str(backup_path), "history.db")

    def backup(self, alias, host: str, port: int, user: str, password: str, database: str, backup_type: str = "full") -> str:
        """
        Realiza el proceso de copia de seguridad para SQLite.
        """
        start_time = datetime.now()
        str_date = start_time.strftime("%Y-%m-%d_%H-%M-%S")
        sql_file = f"backup_{database}_{str_date}.sql"
        compress_file = Path(f"{sql_file}.gz")
        final_path = Path(self.path_base, "sqlite", compress_file)

        try:
            print(f"\nExtrayendo datos de SQLite ({database})...")
            # 1. Hacer backup online consistente de SQLite a un archivo temporal
            temp_db_file = Path(f"{database}_temp_{str_date}.db")
            src_conn = sqlite3.connect(database)
            dest_conn = sqlite3.connect(temp_db_file)
            src_conn.backup(dest_conn)
            dest_conn.close()
            src_conn.close()

            # 3. Comprimir el backup completo
            final_path = compressHandler(temp_db_file, compress_file)
            
            end_time = datetime.now()
            duration = end_time - start_time
            file_size = os.path.getsize(final_path)
            
            historyHandler.add_log(
                alias=alias, 
                engine="sqlite", 
                backup_type="FULL", 
                duration_seconds=duration.total_seconds(), 
                size_bytes=file_size, 
                status="SUCCESS", 
                file_path=str(final_path), 
                storage_destination="local", 
                error_message=None
            )
            if os.path.exists(temp_db_file):
                os.remove(temp_db_file)
            return f"{final_path}"
        except Exception as e:
            end_time = datetime.now()
            duration = end_time - start_time
            err_msg = str(e)
            historyHandler.add_log(
                alias=alias, 
                engine="sqlite", 
                backup_type="FULL", 
                duration_seconds=duration.total_seconds(), 
                size_bytes=0, 
                status="FAILED", 
                file_path=None, 
                storage_destination=None, 
                error_message=err_msg
            )
            if os.path.exists(temp_db_file):
                os.remove(temp_db_file)
            raise RuntimeError(f"Error en backup completo de SQLite: {err_msg}")
