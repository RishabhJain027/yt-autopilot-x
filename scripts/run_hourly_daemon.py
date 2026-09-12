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
    print("=" * 70)
    print("  MAYA ✨ CUTIE BADDIE | 1-HOUR AUTONOMOUS PUBLISHING DAEMON")
    print("  Channel: Maya ✨ Cutie Baddie (@MayaCutieBaddie)")
    print("  Cadence: 1 Video / 3,600 Seconds (1 Hour Interval)")
    print("  Mode: 100% Autonomous (Research -> Script -> SexyVoice -> Render -> YouTube)")
    print("=" * 70)

    await init_db()

    iteration = 1
    while True:
        cycle_start = time.time()
        now_str = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        print(f"\n[{now_str}] >>> Starting Cycle #{iteration}...")

        try:
            await hourly_tick.run_tick()
            await export_telemetry()
            print(f"[{now_str}] <<< Cycle #{iteration} completed successfully.")
        except Exception as e:
            logger.error(f"[DAEMON] Error during cycle #{iteration}: {e}")
            print(f"[ERROR] Cycle #{iteration} encountered error: {e}")

        elapsed = time.time() - cycle_start
        sleep_time = max(0, INTERVAL_SECONDS - elapsed)
        next_run = datetime.now(timezone.utc) + timedelta(seconds=sleep_time)
        print(f"[DAEMON] Sleeping for {sleep_time:.1f}s. Next cycle at: {next_run.strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        
        iteration += 1
        await asyncio.sleep(sleep_time)

if __name__ == "__main__":
    asyncio.run(run_hourly_daemon())