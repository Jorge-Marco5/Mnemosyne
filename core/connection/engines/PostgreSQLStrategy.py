from core.connection.dbConnectionStrategy import DBConnectionStrategy
import subprocess
import os


class PostgreSQLStrategy(DBConnectionStrategy):
    def check_connection(self, host: str, port: int, user: str, password: str, database: str)-> bool:
        """
        Verifica de manera estricta las credenciales y conexión de PostgreSQL.
        """
        env = os.environ.copy()
        if password is not None:
            env["PGPASSWORD"] = password
        
        # -h: host, -p: puerto, -U: usuario, -d: base de datos, -c: comando SQL
        comando = [
            "psql",
            "-h", host,
            "-p", str(port),
            "-U", user,
            "-d", database,
            "-c", "SELECT 1;"
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