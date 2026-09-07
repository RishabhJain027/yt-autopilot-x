import logging
import json
import re
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional

SENSITIVE_PATTERNS = [
    re.compile(r'(password|passwd|pwd)[\"\':=\s]+([^\"\',\s]+)', re.IGNORECASE),
    re.compile(r'(access_token|refresh_token|bearer|authorization)[\"\':=\s]+([^\"\',\s]+)', re.IGNORECASE),
    re.compile(r'(client_secret|api_key|secret_key)[\"\':=\s]+([^\"\',\s]+)', re.IGNORECASE),
]

def sanitize_message(msg: str) -> str:
    cleaned = msg
    for pattern in SENSITIVE_PATTERNS:
        cleaned = pattern.sub(r'\1: [REDACTED]', cleaned)
    return cleaned

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': sanitize_message(record.getMessage()),
        }
        if hasattr(record, 'audit') and record.audit:
            payload['audit_event'] = record.audit
        if record.exc_info:
            payload['exception'] = self.formatException(record.exc_info)
        return json.dumps(payload)

def setup_logger(name: str = 'yt_autopilot', level: str = 'INFO') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
    return logger

logger = setup_logger()

def audit_log(event_type: str, details: Dict[str, Any], channel_id: Optional[str] = None):
    sanitized_details = {k: sanitize_message(str(v)) if isinstance(v, str) else v for k, v in details.items()}
    extra = {
        'audit': {
            'event_type': event_type,
            'channel_id': channel_id,
            'details': sanitized_details,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    }
    logger.info(f'[AUDIT] {event_type}: {json.dumps(sanitized_details)}', extra=extra)
