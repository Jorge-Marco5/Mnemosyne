from core.service_storage.serviceStorageStrategy import ServiceStorageStrategy
import os
from pathlib import Path
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# Cargar variables de entorno
load_dotenv()

class AzureStorageStrategy(ServiceStorageStrategy):
    def upload(self, backup_file: str):
        """
        Realiza el proceso de carga del archivo de respaldo a Azure Blob Storage
        """
        azure_storage_key = os.getenv('AZURE_STORAGE_KEY')
        azure_account_name = os.getenv('AZURE_STORAGE_ACCOUNT')
        azure_container_name = os.getenv('AZURE_CONTAINER_NAME')

        connect_str = f"DefaultEndpointsProtocol=https;AccountName={azure_account_name};AccountKey={azure_storage_key};EndpointSuffix=core.windows.net"

        try:
            print(f"\nSubiendo {backup_file} a Azure Blob Storage...")
            # Crear el objeto BlobServiceClient usando la cadena de conexión
            blob_service_client = BlobServiceClient.from_connection_string(connect_str)

            # Crear un cliente para el blob
            blob_client = blob_service_client.get_blob_client(container=str(azure_container_name), blob=backup_file)

            # Subir el archivo
            with open(backup_file, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            os.remove(backup_file)
            
            print(f"¡Respaldo subido con éxito a Azure Blob Storage!")
            return True
        except Exception as e:
            print(f"Ocurrió un error al subir a Azure Blob Storage: {e}")
            return False

    def download(self, remote_file_name: str, local_dest_path: str) -> bool:
        """
        Realiza el proceso de descarga del archivo de respaldo de Azure Blob Storage
        """
        azure_storage_key = os.getenv('AZURE_STORAGE_KEY')
        azure_account_name = os.getenv('AZURE_STORAGE_ACCOUNT')
        azure_container_name = os.getenv('AZURE_CONTAINER_NAME')

        connect_str = f"DefaultEndpointsProtocol=https;AccountName={azure_account_name};AccountKey={azure_storage_key};EndpointSuffix=core.windows.net"

        try:
            print(f"\nDescargando {remote_file_name} desde Azure Blob Storage a {local_dest_path}...")
            # Asegurar que el directorio local existe
            Path(local_dest_path).parent.mkdir(parents=True, exist_ok=True)
            
            blob_service_client = BlobServiceClient.from_connection_string(connect_str)
            blob_client = blob_service_client.get_blob_client(container=str(azure_container_name), blob=remote_file_name)

            with open(local_dest_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
                
            print("¡Respaldo descargado con éxito desde Azure Blob Storage!")
            return True
        except Exception as e:
            print(f"Ocurrió un error al descargar desde Azure Blob Storage: {e}")
            return False