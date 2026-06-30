from core.connection.dbConnectionStrategy import DBConnectionStrategy
import sqlite3

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