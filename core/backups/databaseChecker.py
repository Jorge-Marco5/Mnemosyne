from core.backups.dbBackupStrategy import DBBackupStrategy
from core.backups.engines.PostgreSQLStrategy import PostgreSQLStrategy
from core.backups.engines.MySQLStrategy import MySQLStrategy
from core.backups.engines.SQLiteStrategy import SQLiteStrategy


class DatabaseBackupChecker:
    def __init__(self):
        self._strategies = {
            "postgresql": PostgreSQLStrategy(),
            "mysql": MySQLStrategy(),
            "sqlite": SQLiteStrategy()
        }
    
    def register_strategy(self, name: str, strategy: DBBackupStrategy):
        """Permite agregar nuevos tipos de bases de datos externamente."""
        self._strategies[name.lower()] = strategy

    def verify(self, alias , db_type: str, host: str, port: int, user: str, password: str, database: str) -> str:
        """Obtiene la estrategia según el nombre y ejecuta el check."""
        strategy = self._strategies.get(db_type.lower())
        
        if not strategy:
            raise ValueError(f"Gestor de base de datos '{db_type}' no soportado.")
            
        return strategy.backup(alias, host, port, user, password, database)
    
    def get_strategies(self):
        """
        Obtiene la lista de estrategias actual
        """
        return self._strategies.keys()
    
