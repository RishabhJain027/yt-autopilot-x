import json
import os
from datetime import datetime, timezone
from typing import Dict, Any
from packages.config.settings import settings
from packages.logger.logger import logger

DAILY_LIMIT = 10000

# YouTube API v3 standard unit costs
COSTS = {
    'videos.insert': 1600,
    'thumbnails.set': 50,
    'videos.update': 50,
    'videos.list': 1,
    'channels.list': 1,
    'search.list': 100,
    'playlists.list': 1,
    'analytics.query': 10,
}

class QuotaManager:
    def __init__(self, storage_path: str = None):
        self.path = storage_path or os.path.join(settings.STORAGE_ROOT, 'quota_tracker.json')
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {}
        else:
            self.data = {}

        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        if self.data.get('date') != today:
            self.data = {
                'date': today,
                'used': 0,
                'limit': DAILY_LIMIT,
                'calls': []
            }
            self._save()

    def _save(self):
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f'Failed to save quota state: {e}')

    def get_remaining_quota(self) -> int:
        self._load()
        return max(0, self.data['limit'] - self.data['used'])

    def can_afford(self, operation: str) -> bool:
        cost = COSTS.get(operation, 100)
        return self.get_remaining_quota() >= cost

    def consume(self, operation: str, details: str = '') -> bool:
        self._load()
        cost = COSTS.get(operation, 100)
        if self.data['used'] + cost > self.data['limit']:
            logger.warning(f'Quota exceeded: cannot perform {operation} (cost {cost}, remaining {self.get_remaining_quota()})')
            return False

        self.data['used'] += cost
        self.data['calls'].append({
            'operation': operation,
            'cost': cost,
            'time': datetime.now(timezone.utc).isoformat(),
            'details': details
        })
        self._save()
        logger.info(f'[QUOTA] Consumed {cost} for {operation}. Remaining: {self.get_remaining_quota()}/{self.data["limit"]}')
        return True

quota_manager = QuotaManager()
