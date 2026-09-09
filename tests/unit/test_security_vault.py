import pytest
import sys, os
from urllib.parse import urlparse
sys.path.insert(0, '.')
from python.services.credential_vault import CredentialVault
from packages.logger.logger import sanitize_message
from python.research.url_fetcher import SafeUrlFetcher, PRIVATE_IP_REGEX

def test_credential_encryption_decryption():
    vault = CredentialVault()
    raw_token = "ya29.test-sample-oauth-token"
    enc = vault.encrypt_token(raw_token)
    dec = vault.decrypt_token(enc)
    assert dec == raw_token
    assert "ya29" not in enc

def test_log_token_redaction():
    redacted = sanitize_message("User access_token='ya29.secret12345' logged in")
    assert "ya29" not in redacted
    assert "[REDACTED]" in redacted

def test_ssrf_blocks_private_ips():
    fetcher = SafeUrlFetcher()
    assert bool(PRIVATE_IP_REGEX.match(urlparse("http://127.0.0.1/admin").hostname)) is True
    assert bool(PRIVATE_IP_REGEX.match(urlparse("http://192.168.1.1/secret").hostname)) is True
    assert bool(PRIVATE_IP_REGEX.match(urlparse("https://www.google.com").hostname)) is False

