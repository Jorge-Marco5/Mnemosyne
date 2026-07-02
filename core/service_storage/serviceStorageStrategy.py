from abc import ABC, abstractmethod

class ServiceStorageStrategy(ABC):
    """
    Interfaz abstracta para las estrategias de servicios de almacenamiento externos.
    """
    @abstractmethod
    def upload(self, backup_file: str) -> bool:
        """Define el método para cargar un archivo de respaldo a un servicio de almacenamiento externo."""
        pass