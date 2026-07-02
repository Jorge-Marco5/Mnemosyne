from core.backups.dbBackupStrategy import DBBackupStrategy
import os
import subprocess
from pathlib import Path
from datetime import datetime
from core.compress import compressHandler

class MySQLStrategy(DBBackupStrategy):
    backup_path = os.getenv("BACKUPS_PATH", "backups")
    path_base = Path(str(backup_path))

    def backup(self, alias, upload_service: str, host: str, port: int, user: str, password: str, database: str, backup_type: str = "full") -> dict:
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

        env = os.environ.copy()
        if password is not None:
            env["MYSQL_PWD"] = password

        comando = [
            "mysqldump",
            "-h", host,
            "-P", str(port),
            "-u", user,
            database
        ]

        try:
            print(f"\nExtrayendo datos de MySQL ({database})...")
            with open(sql_path, "w", encoding="utf-8") as f_out:
                subprocess.run(comando, env=env, stdout=f_out, stderr=subprocess.PIPE, check=True)

            file_path = compressHandler(sql_path, final_path)
            end_time = datetime.now()
            duration = end_time - start_time
            file_size = os.path.getsize(file_path) if file_path and os.path.exists(file_path) else 0

            return {
                "alias": alias,
                "engine": "mysql",
                "backup_type": backup_type.upper(),
                "duration_seconds": duration.total_seconds(),
                "size_bytes": file_size,
                "file_path": str(file_path) if file_path else None
            }
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.decode('utf-8', errors='replace') if e.stderr else str(e)
            if sql_path.exists():
                os.remove(sql_path)
            raise RuntimeError(f"Error en mysqldump: {err_msg}")
        except Exception as e:
            if sql_path.exists():
                os.remove(sql_path)
            raise RuntimeError(f"Error en backup de MySQL: {str(e)}")