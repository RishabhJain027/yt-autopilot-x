import httpx
import re
from urllib.parse import urlparse
from typing import Optional
from packages.logger.logger import logger

PRIVATE_IP_REGEX = re.compile(
    r'^(localhost|127\.\d+\.\d+\.\d+|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(1[6-9]|2\d|3[0-1])\.\d+\.\d+|0\.0\.0\.0|::1)$',
    re.IGNORECASE
)

class SafeUrlFetcher:
    def __init__(self, timeout_seconds: float = 10.0, max_bytes: int = 2 * 1024 * 1024):
        self.timeout = timeout_seconds
        self.max_bytes = max_bytes

    async def fetch_text(self, url: str) -> Optional[str]:
        try:
            parsed = urlparse(url)
            if parsed.scheme not in ('http', 'https'):
                logger.warning(f'[SECURITY] Rejected unsafe scheme: {parsed.scheme} for URL {url}')
                return None
            hostname = parsed.hostname or ''
            if PRIVATE_IP_REGEX.match(hostname):
                logger.warning(f'[SECURITY] SSRF protection blocked access to internal host: {hostname}')
                return None

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) YT-Autopilot-X/1.0'}
            async with httpx.AsyncClient(follow_redirects=True, timeout=self.timeout) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code != 200:
                    logger.warning(f'Failed to fetch URL {url}: HTTP {resp.status_code}')
                    return None
                if len(resp.content) > self.max_bytes:
                    logger.warning(f'URL response exceeded size limit: {len(resp.content)} bytes')
                    return resp.text[:self.max_bytes]
                return resp.text
        except Exception as e:
            logger.error(f'Error fetching URL {url}: {e}')
            return None

safe_fetcher = SafeUrlFetcher()
