from core.connection.dbConnectionStrategy import DBConnectionStrategy
from core.connection.engines.PostgreSQLStrategy import PostgreSQLStrategy
from core.connection.engines.MySQLStrategy import MySQLStrategy
from core.connection.engines.SQLIteStrategy import SQLiteStrategy

class DatabaseConnectionChecker:
    def __init__(self):
        self._strategies = {
            "postgresql": PostgreSQLStrategy(),
            "mysql": MySQLStrategy(),
            "sqlite": SQLiteStrategy()
        }
    
    def register_strategy(self, name: str, strategy: DBConnectionStrategy):
        """Permite agregar nuevos tipos de bases de datos externamente."""
        self._strategies[name.lower()] = strategy

    def verify(self, db_type: str, host: str, port: int, user: str, password: str, database: str) -> bool:
        """Obtiene la estrategia según el nombre y ejecuta el check."""
        strategy = self._strategies.get(db_type.lower())
        
        if not strategy:
            raise ValueError(f"Gestor de base de datos '{db_type}' no soportado.")
            
        return strategy.check_connection(host, port, user, password, database)
    
    def get_strategies(self):
        """
        Obtiene la lista de estrategias actual
        """
        return self._strategies.keys()
    
