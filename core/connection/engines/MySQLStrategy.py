from core.connection.dbConnectionStrategy import DBConnectionStrategy
import subprocess
import os


class MySQLStrategy(DBConnectionStrategy):
    def check_connection(self, host: str, port: int, user: str, password: str, database: str)-> bool:
        """
        Verifica de manera estricta las credenciales y conexión de MySQL.
        """
        env = os.environ.copy()
        if password is not None:
            env["MYSQL_PWD"] = password
            
        # Construir el comando mysql
        # -h: host, -P: puerto, -u: usuario, -D: base de datos, -e: ejecutar consulta
        comando = [
            "mysql",
            "-h", host,
            "-P", str(port),
            "-u", user,
            "-D", database,
            "-e", "SELECT 1;"
        ]
        try:
            resultado = subprocess.run(
                comando, 
                env=env,
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL, 
                timeout=5
            )
            # Retorna True si la conexión y autenticación fueron exitosas (código 0)
            return resultado.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False