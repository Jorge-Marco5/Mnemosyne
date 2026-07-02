from core.backups.dbBackupStrategy import DBBackupStrategy
import os
import sqlite3
from pathlib import Path
from datetime import datetime
from core.compress import compressHandler

class SQLiteStrategy(DBBackupStrategy):
    backup_path = os.getenv("BACKUPS_PATH", "backups")
    path_base = Path(str(backup_path))

    def backup(self, alias, upload_service: str, host: str, port: int, user: str, password: str, database: str, backup_type: str = "full") -> dict:
        """
        Realiza el proceso de copia de seguridad para SQLite.
        """
        start_time = datetime.now()
        str_date = start_time.strftime("%Y-%m-%d_%H-%M-%S")
        db_name = Path(database).name
        sql_file = f"backup_{db_name}_{str_date}.sql"
        compress_file = Path(f"{sql_file}.gz")
        out_path = Path(self.path_base, "sqlite")
        final_path = Path(out_path, compress_file)

        out_path.mkdir(parents=True, exist_ok=True)
        temp_db_file = Path(out_path, f"temp_{db_name}_{str_date}.db")

        try:
            print(f"\nExtrayendo datos de SQLite ({database})...")
            src_conn = sqlite3.connect(database)
            dest_conn = sqlite3.connect(str(temp_db_file))
            src_conn.backup(dest_conn)
            dest_conn.close()
            src_conn.close()

            file_path = compressHandler(temp_db_file, final_path)
            
            end_time = datetime.now()
            duration = end_time - start_time
            file_size = os.path.getsize(file_path) if file_path and os.path.exists(file_path) else 0
            
            if temp_db_file.exists():
                os.remove(temp_db_file)

            return {
                "alias": alias,
                "engine": "sqlite",
                "backup_type": backup_type.upper(),
                "duration_seconds": duration.total_seconds(),
                "size_bytes": file_size,
                "file_path": str(file_path) if file_path else None
            }
        except Exception as e:
            if temp_db_file.exists():
                os.remove(temp_db_file)
            raise RuntimeError(f"Error en backup de SQLite: {str(e)}")
