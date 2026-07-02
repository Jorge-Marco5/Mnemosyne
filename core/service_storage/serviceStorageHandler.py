from core.service_storage.services.AWSS3Strategy import AwsS3Strategy
from core.service_storage.services.AzureStorageStrategy import AzureStorageStrategy

class ServiceStorageHandler:
    """
    Clase que gestiona y ejecuta la estrategia de restauración apropiada.
    """
    def __init__(self):
        self._strategies = {
            "aws-s3": AwsS3Strategy(),
            "azure-storage": AzureStorageStrategy(),
        }

    def verify(self, service: str, backup_file: str) -> bool:
        """
        Selecciona y ejecuta la estrategia de restauración para el motor de DB dado.
        """
        strategy = self._strategies.get(service)
        if not strategy:
            raise ValueError(f"Servicio no soportado para carga: {service}")
        
        return strategy.upload(backup_file)