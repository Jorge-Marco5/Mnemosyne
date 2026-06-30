import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
from dotenv import load_dotenv

load_dotenv()

def getMasterKey():
    clave_str = os.getenv("BACKUP_MASTER_KEY")
    if clave_str is None:
        raise ValueError("BACKUP_MASTER_KEY no está configurada en las variables de entorno.")
    return base64.urlsafe_b64decode(clave_str)

def encriptText(text):
    """
    Encripta el texto ingresado por el usuario
    """
    key = getMasterKey()
    aesgcm = AESGCM(key)
    nonce = os.urandom(16)
    ciphertext = aesgcm.encrypt(nonce, text.encode('utf-8'), None)
    return base64.urlsafe_b64encode(nonce + ciphertext).decode('utf-8')

def decriptText(text):
    """
    Desencripta el texto ingresado por el usuario
    """
    key = getMasterKey()
    decoded_text = base64.urlsafe_b64decode(text)
    nonce = decoded_text[:16]
    ciphertext = decoded_text[16:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')

    