from abc import ABC, abstractmethod

class DBRestoreStrategy(ABC):
    """
    Interfaz abstracta para las estrategias de restauración de bases de datos.
    """
    @abstractmethod
    def restore(self, host: str, port: int, user: str, password: str, database: str, backup_file: str) -> bool:
        """Define el método para restaurar una base de datos desde un archivo."""
        pass