from core.restore.dbRestoreStrategy import DBRestoreStrategy
import subprocess
from pathlib import Path

class MySQLStrategy(DBRestoreStrategy):
    def restore(self, host: str, port: int, user: str, password: str, database: str, backup_file: str) -> bool:
        """
        Realiza el proceso de restauración para MySQL desde un archivo .gz.
        """
        backup_path = Path(backup_file)

        # Usar un pipeline de shell para descomprimir y pasar a mysql directamente
        comando_str = f"gunzip < {backup_path.resolve()} | mysql -h {host} -P {port} -u {user} -p'{password}' {database}"

        print(f"Restaurando base de datos MySQL '{database}'...")
        
        resultado = subprocess.run(
            comando_str, 
            shell=True,
            check=True, 
            capture_output=True, 
            text=True
        )

        if resultado.returncode != 0:
            raise subprocess.CalledProcessError(resultado.returncode, comando_str, stderr=resultado.stderr)
        
        return True