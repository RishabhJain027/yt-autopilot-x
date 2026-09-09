import sys
import os
import time
import asyncio
from datetime import datetime, timezone, timedelta
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from packages.config.settings import settings
from packages.logger.logger import logger
from database.connection import init_db
from python.pipelines.hourly_tick import hourly_tick
from scripts.export_telemetry import export_telemetry

INTERVAL_SECONDS = 3600  # 1 Hour Cadence

async def run_hourly_daemon(immediate: bool = True):
    print('=' * 70)
    print('  MAYA ✄ CUTIE BADDIE | 1-HOUR AUTONOLOUS PUBLISHING DAEMON')
    print('  Channel: Maya ✄ Cutie Baddie (@MayaCutieBaddie)')
    print('  Cadence: 1 Video / 3,600 Seconds (1 Hour Interval)')
    print('  Mode: 100%