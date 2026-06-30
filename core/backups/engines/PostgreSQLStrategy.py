from core.backups.dbBackupStrategy import DBBackupStrategy
from core.compress import compressHandler
import os
import subprocess
from pathlib import Path
from datetime import datetime
from core.data_service import DataService
from dotenv import load_dotenv

load_dotenv()

historyHandler = DataService()

class PostgreSQLStrategy(DBBackupStrategy):
    BACKUPS_PATH = os.getenv("BACKUPS_PATH")
    path_base = Path(str(BACKUPS_PATH))
    #path_base = os.environ.get("BACKUPS_PATH", "backups")
    def backup(self, alias, host: str, port: int, user: str, password: str, database: str, backup_type: str = "full") -> str|None:
        """
        Realiza el proceso de copia de seguridad para PostgreSQL.
        """
        start_time = datetime.now()
        str_date = start_time.strftime("%Y-%m-%d_%H-%M-%S")
        out_path = Path(self.path_base, "postgresql")
        sql_file = Path(f"backup_{database}_{str_date}.sql")
        compress_file = Path(f"backup_{database}_{str_date}.gz")
        sql_path=Path(out_path, sql_file)
        final_path = Path(Path(out_path, compress_file))

        out_path.mkdir(parents=True, exist_ok=True)

        env = os.environ.copy()
        env["PGPASSWORD"] = password
        
        comando = [
            "pg_dump",
            "-h", host,
            "-p", str(port),
            "-U", user,
            "-F", "p", 
            "-f", sql_path,
            database
        ]

        try:
            print(f"\nExtrayendo datos de PostgreSQL ({database})...")
            resultado = subprocess.run(comando, env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            file_path = compressHandler(sql_path, final_path)

            end_time = datetime.now()
            duration = end_time - start_time
            file_size = os.path.getsize(file_path)
            
            historyHandler.add_log(
                alias=alias, 
                engine="postgresql", 
                backup_type=backup_type.upper(), 
                duration_seconds=duration.total_seconds(), 
                size_bytes=file_size, 
                status="SUCCESS", 
                file_path=str(file_path), 
                storage_destination="local", 
                error_message=None
            )

            return f"{file_path}"
        except subprocess.CalledProcessError as e:
            end_time = datetime.now()
            duration = end_time - start_time
            err_msg = e.stderr.decode('utf-8', errors='replace') if e.stderr else str(e)
            historyHandler.add_log(
                alias=alias, 
                engine="postgresql", 
                backup_type=backup_type.upper(), 
                duration_seconds=duration.total_seconds(), 
                size_bytes=0, 
                status="FAILED", 
                file_path=None, 
                storage_destination=None, 
                error_message=err_msg
            )
        except Exception as e:
            end_time = datetime.now()
            duration = end_time - start_time
            err_msg = str(e)
            historyHandler.add_log(
                alias=alias, 
                engine="postgresql", 
                backup_type=backup_type.upper(), 
                duration_seconds=duration.total_seconds(), 
                size_bytes=0, 
                status="FAILED", 
                file_path=None, 
                storage_destination=None, 
                error_message=err_msg
            )
            raise RuntimeError(f"Error en backup físico de PostgreSQL: {err_msg}")