from core.backups.dbBackupStrategy import DBBackupStrategy
import os
import subprocess
from pathlib import Path
from datetime import datetime
from core.compress import compressHandler
from core.data_service import DataService

historyHandler = DataService()


class MySQLStrategy(DBBackupStrategy):
    backup_path = os.getenv("BACKUPS_PATH")
    path_base = Path(str(backup_path))
    def backup(self, alias, host: str, port: int, user: str, password: str, database: str, backup_type: str = "full") -> str|None:
        """
        Realiza el proceso de copia de seguridad para MySQL.

        """
        start_time = datetime.now()
        str_date = start_time.strftime("%Y-%m-%d_%H-%M-%S")
        out_path = Path(self.path_base, "mysql")
        sql_file = Path(f"backup_{database}_{str_date}.sql")
        compress_file = Path(f"backup_{database}_{str_date}.gz")
        sql_path = Path(out_path, sql_file)
        final_path = Path(out_path, compress_file)

        out_path.mkdir(parents=True, exist_ok=True)

        comando = [
            "mysqldump",
            "-h", host,
            "-P", str(port),
            "-u", user,
            f"-p{password}",
            database
        ]

        try:
            print(f"\nExtrayendo datos de MySQL ({database})...")
            with open(sql_path, "w", encoding="utf-8") as f_out:
                subprocess.run(comando, stdout=f_out, stderr=subprocess.PIPE, check=True)

            final_path = compressHandler(sql_path, final_path)
            end_time = datetime.now()
            duration = end_time - start_time
            file_size = os.path.getsize(final_path)

            historyHandler.add_log(
                alias=alias, 
                engine="mysql", 
                backup_type="FULL", 
                duration_seconds=duration.total_seconds(), 
                size_bytes=file_size, 
                status="SUCCESS", 
                file_path=str(final_path), 
                storage_destination="local", 
                error_message=None
            )

            return f"{final_path}"
        except subprocess.CalledProcessError as e:
            end_time = datetime.now()
            duration = end_time - start_time
            err_msg = e.stderr.decode('utf-8', errors='replace') if e.stderr else str(e)
            historyHandler.add_log(
                alias=alias, 
                engine="mysql", 
                backup_type="FULL", 
                duration_seconds=duration.total_seconds(), 
                size_bytes=0, 
                status="FAILED", 
                file_path=None, 
                storage_destination=None, 
                error_message=err_msg
            )
            if os.path.exists(sql_file):
                os.remove(sql_file)
            raise RuntimeError(f"Error en mysqldump: {err_msg}")
        except Exception as e:
            end_time = datetime.now()
            duration = end_time - start_time
            err_msg = str(e)
            historyHandler.add_log(
                alias=alias, 
                engine="mysql", 
                backup_type="FULL", 
                duration_seconds=duration.total_seconds(), 
                size_bytes=0, 
                status="FAILED", 
                file_path=None, 
                storage_destination=None, 
                error_message=err_msg
            )
            if os.path.exists(sql_file):
                os.remove(sql_file)
            raise RuntimeError(f"Error en backup de MySQL: {err_msg}")