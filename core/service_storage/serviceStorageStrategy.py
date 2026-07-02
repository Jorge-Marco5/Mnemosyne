from abc import ABC, abstractmethod

class ServiceStorageStrategy(ABC):
    """
    Interfaz abstracta para las estrategias de servicios de almacenamiento externos.
    """
    @abstractmethod
    def upload(self, backup_file: str) -> bool:
        """Define el método para cargar un archivo de respaldo a un servicio de almacenamiento externo."""
        pass

    @abstractmethod
    def download(self, remote_file_name: str, local_dest_path: str) -> bool:
        """Define el método para descargar un archivo de respaldo desde un servicio de almacenamiento externo."""
        pass