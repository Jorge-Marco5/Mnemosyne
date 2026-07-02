from core.service_storage.serviceStorageStrategy import ServiceStorageStrategy
import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError

# Cargar variables de entorno
load_dotenv()

class AwsS3Strategy(ServiceStorageStrategy):
    def upload(self, backup_file: str):
        """
        Realiza el proceso de carga del archivo de respaldo a AWS S3
        """
        secret_key = os.getenv('AWS_SECRET_KEY')
        secret_access_key = os.getenv('AWS_ACCESS_KEY')
        region_name = os.getenv('AWS_REGION')
        bucket_name = os.getenv('AWS_BUCKET_NAME')
        folder_name = os.getenv('AWS_FOLDER_NAME', '')  # Carpeta opcional en el bucket

        s3 = boto3.client(
            's3',
            aws_access_key_id=str(secret_access_key),
            aws_secret_access_key=str(secret_key),
            region_name=str(region_name)
        )

        try:
            print(f"\nSubiendo {backup_file} a AWS S3...")
            s3.upload_file(backup_file, str(bucket_name), f"{folder_name}/{os.path.basename(backup_file)}" if folder_name else os.path.basename(backup_file))
            os.remove(backup_file)
            print("¡Respaldo subido con éxito a AWS S3!")
            return True
        except FileNotFoundError:
            print("El archivo local no fue encontrado.")
            return False
        except NoCredentialsError:
            print("Credenciales no válidas o no encontradas.")
            return False
        except Exception as e:
            print(f"Ocurrió un error al subir a AWS S3: {e}")
            return False