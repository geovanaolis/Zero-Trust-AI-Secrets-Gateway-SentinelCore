import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

class EnvelopeCryptoManager:
    """
    Gerenciador de Criptografia de Segurança.
    Utiliza uma chave mestre (Master Key) para derivar chaves de criptografia 
    simétrica e proteger os segredos armazenados no cofre.
    """
    
    def __init__(self, master_secret: str, salt: bytes = None):
        # Em produção, o SALT deve ser único por secret ou armazenado de forma segura
        self.salt = salt or b'sentinel_static_salt_2026'
        self.key = self._derive_key(master_secret)
        self.fernet = Fernet(self.key)

    def _derive_key(self, master_secret: str) -> bytes:
        """Deriva uma chave simétrica segura usando PBKDF2 com SHA-256."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(master_secret.encode()))

    def encrypt(self, plain_text: str) -> str:
        """Criptografa uma string pura e retorna a cifra em Base64."""
        if not plain_text:
            return ""
        return self.fernet.encrypt(plain_text.encode()).decode()

    def decrypt(self, cipher_text: str) -> str:
        """Descriptografa uma cifra e devolve a string original."""
        if not cipher_text:
            return ""
        return self.fernet.decrypt(cipher_text.encode()).decode()