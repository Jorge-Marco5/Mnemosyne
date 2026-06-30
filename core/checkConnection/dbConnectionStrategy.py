from abc import ABC, abstractmethod
import subprocess
import os
import sqlite3

class DBConnectionStrategy(ABC):
    @abstractmethod    
    def check_connection(self, host: str, port: int, user: str, password: str, database: str) -> bool:
        """
        Abstract method to check the connection to a database.
        """
        pass

class PostgreSQLStrategy(DBConnectionStrategy):
    def check_connection(self, host: str, port: int, user: str, password: str, database: str)-> bool:
        """
        Verifica de manera estricta las credenciales y conexión de PostgreSQL.
        Ejecuta una consulta de prueba ('SELECT 1;') para obligar la autenticación.
        """
        env = os.environ.copy()
        if password is not None:
            env["PGPASSWORD"] = password
        
        # Construir el comando psql
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
            # Ejecutar psql
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
        
class MySQLStrategy(DBConnectionStrategy):
    def check_connection(self, host: str, port: int, user: str, password: str, database: str)-> bool:
        """
        Verifica de manera estricta las credenciales y conexión de MySQL.
        Ejecuta una consulta de prueba ('SELECT 1;') para obligar la autenticación.
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

class SQLiteStrategy(DBConnectionStrategy):
    def check_connection(self, host: str|None, port: int|None, user: str|None, password: str|None, database: str) -> bool:
        """
        Verifica la conexión a una base de datos SQLite (validando que el archivo sea accesible).
        """
        if not database:
            return False
        try:
            # Intentar abrir la conexión al archivo de base de datos
            conn = sqlite3.connect(database)
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            cursor.close()
            conn.close()
            return True
        except Exception:
            return False