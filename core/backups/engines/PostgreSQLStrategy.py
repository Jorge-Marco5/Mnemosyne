from core.backups.dbBackupStrategy import DBBackupStrategy
from core.compress import compressHandler
import os
import subprocess
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class PostgreSQLStrategy(DBBackupStrategy):
    BACKUPS_PATH = os.getenv("BACKUPS_PATH", "backups")
    path_base = Path(str(BACKUPS_PATH))

    def backup(self, alias, upload_service: str, host: str, port: int, user: str, password: str, database: str, backup_type: str = "full") -> dict:
        """
        Realiza el proceso de copia de seguridad para PostgreSQL.
        """
        start_time = datetime.now()
        str_date = start_time.strftime("%Y-%m-%d_%H-%M-%S")
        out_path = Path(self.path_base, "postgresql")
        sql_file = Path(f"backup_{database}_{str_date}.sql")
        compress_file = Path(f"backup_{database}_{str_date}.gz")
        sql_path = Path(out_path, sql_file)
        final_path = Path(out_path, compress_file)

        out_path.mkdir(parents=True, exist_ok=True)

        env = os.environ.copy()
        if password is not None:
            env["PGPASSWORD"] = password
        
        comando = [
            "pg_dump",
            "-h", host,
            "-p", str(port),
            "-U", user,
            "-F", "p", 
            "-f", str(sql_path),
            database
        ]

        try:
            print(f"\nExtrayendo datos de PostgreSQL ({database})...")
            subprocess.run(comando, env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            file_path = compressHandler(sql_path, final_path)

            end_time = datetime.now()
            duration = end_time - start_time
            file_size = os.path.getsize(file_path) if file_path and os.path.exists(file_path) else 0
            
            return {
                "alias": alias,
                "engine": "postgresql",
                "backup_type": backup_type.upper(),
                "duration_seconds": duration.total_seconds(),
                "size_bytes": file_size,
                "file_path": str(file_path) if file_path else None
            }
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.decode('utf-8', errors='replace') if e.stderr else str(e)
            if sql_path.exists():
                os.remove(sql_path)
            raise RuntimeError(f"Error en pg_dump: {err_msg}")
        except Exception as e:
            if sql_path.exists():
                os.remove(sql_path)
            raise RuntimeError(f"Error en backup de PostgreSQL: {str(e)}")