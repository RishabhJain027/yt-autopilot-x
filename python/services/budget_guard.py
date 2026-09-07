import json
import os
from datetime import datetime, timezone
from packages.config.settings import settings
from packages.logger.logger import logger

class BudgetGuard:
    def __init__(self, storage_path: str = None):
        self.path = storage_path or os.path.join(settings.STORAGE_ROOT, 'budget_tracker.json')
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
        month = datetime.now(timezone.utc).strftime('%Y-%m')
        if self.data.get('date') != today:
            self.data['date'] = today
            self.data['daily_spent'] = 0.0
        if self.data.get('month') != month:
            self.data['month'] = month
            self.data['monthly_spent'] = 0.0
        self.data.setdefault('daily_spent', 0.0)
        self.data.setdefault('monthly_spent', 0.0)
        self.data.setdefault('records', [])

    def _save(self):
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f'Failed to save budget state: {e}')

    def estimate_cost(self, job_type: str, units: int = 1) -> float:
        # Standard unit costs in USD
        rates = {
            'llm_tokens_1k': 0.0015,
            'tts_char_1k': 0.015,
            'image_generation': 0.04,
            'video_seconds_10': 0.10,
        }
        return rates.get(job_type, 0.01) * units

    def can_spend(self, amount_usd: float) -> bool:
        self._load()
        if (self.data['daily_spent'] + amount_usd) > settings.DAILY_BUDGET_USD:
            logger.warning(f'Budget blocked: Daily budget of ${settings.DAILY_BUDGET_USD} would be exceeded')
            return False
        if (self.data['monthly_spent'] + amount_usd) > settings.MONTHLY_BUDGET_USD:
            logger.warning(f'Budget blocked: Monthly budget of ${settings.MONTHLY_BUDGET_USD} would be exceeded')
            return False
        return True

    def record_spend(self, provider: str, job_type: str, amount_usd: float, job_id: str = ''):
        self._load()
        self.data['daily_spent'] += amount_usd
        self.data['monthly_spent'] += amount_usd
        self.data['records'].append({
            'provider': provider,
            'job_type': job_type,
            'amount_usd': amount_usd,
            'job_id': job_id,
            'time': datetime.now(timezone.utc).isoformat()
        })
        self._save()
        logger.info(f'[BUDGET] Spent ${amount_usd:.4f} on {provider} ({job_type}). Today: ${self.data["daily_spent"]:.2f}/${settings.DAILY_BUDGET_USD}')

budget_guard = BudgetGuard()
