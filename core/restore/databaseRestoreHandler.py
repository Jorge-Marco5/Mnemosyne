from core.restore.engines.PostgreSQLStrategy import PostgreSQLStrategy
from core.restore.engines.MySQLStrategy import MySQLStrategy
from core.restore.engines.SQLiteStrategy import SQLiteStrategy

class DatabaseRestoreHandler:
    """
    Clase que gestiona y ejecuta la estrategia de restauración apropiada.
    """
    def __init__(self):
        self._strategies = {
            "postgresql": PostgreSQLStrategy(),
            "mysql": MySQLStrategy(),
            "sqlite": SQLiteStrategy(),
        }

    def restore(self, engine: str, host: str, port: int, user: str, password: str, database: str, backup_file: str) -> bool:
        """
        Selecciona y ejecuta la estrategia de restauración para el motor de DB dado.
        """
        strategy = self._strategies.get(engine)
        if not strategy:
            raise ValueError(f"Motor de base de datos no soportado para restauración: {engine}")
        
        return strategy.restore(host, port, user, password, database, backup_file)