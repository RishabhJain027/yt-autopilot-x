import base64
import os
from typing import Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from packages.config.settings import settings

class CredentialVault:
    def __init__(self, secret_key_hex: Optional[str] = None):
        hex_key = secret_key_hex or settings.SECRET_KEY
        if len(hex_key) < 64:
            hex_key = hex_key.ljust(64, '0')
        self.key = bytes.fromhex(hex_key[:64])
        self.aesgcm = AESGCM(self.key)

    def encrypt_token(self, plaintext: str) -> str:
        if not plaintext:
            return ''
        nonce = os.urandom(12)
        ciphertext = self.aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
        bundle = nonce + ciphertext
        return base64.b64encode(bundle).decode('utf-8')

    def decrypt_token(self, encrypted_b64: str) -> str:
        if not encrypted_b64:
            return ''
        try:
            bundle = base64.b64decode(encrypted_b64.encode('utf-8'))
            nonce = bundle[:12]
            ciphertext = bundle[12:]
            decrypted = self.aesgcm.decrypt(nonce, ciphertext, None)
            return decrypted.decode('utf-8')
        except Exception as e:
            raise ValueError('Decryption failed: Token is invalid or key mismatch') from e

vault = CredentialVault()
