import pytest
import sys, os
sys.path.insert(0, '.')
from python.services.credential_vault import CredentialVault
from packages.logger.logger import StructuredLogger
from python.research.url_fetcher import SafeURLFetcher

def test_credential_encryption_decryption():
    vault = CredentialVault()
    secret_token = {'access_token': 'ya29.test-otaken-12345', 'refresh_token': '1//test-refresh-token'}
    encrypted = vault.encrypt(secret_token)
    assert encrypted != secret_token
    assert 'ya29' not in encrypted
    decrypted = vault.decrypt(encrypted)
    assert decrypted == secret_token

def test_log_token_redaction():
    logger = StructuredLogger()
    sample_msg = "Connected with token ya29.abcd123456 and secret secret_key=999888777"
    redacted = logger._redact(sample_msg)
    assert 'ya29' not in redacted
    assert '[REDACTED]' in redacted

def test_ssrf_blocks_private_ips():
    fetcher = SafeURLFetcher()
    assert fetcher.is_safe_url("http://127.0.0.1/admin") == False
    assert fetcher.is_safe_url("http://192.168.1.1/status") == False
    assert fetcher.is_safe_url("http://169.254.169.254/latest/meta-data/") == False
    assert fetcher.is_safe_url("https://www.wikipedia.org") == True

