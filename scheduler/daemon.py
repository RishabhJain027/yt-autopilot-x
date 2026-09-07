import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from packages.config.settings import settings
from packages.logger.logger import logger
from python.pipelines.hourly_tick import hourly_tick

scheduler = AsyncIOScheduler(timezone=settings.SCHEDULER_TIMEZONE)

async def tick_job():
    try:
        await hourly_tick.run_tick()
    except Exception as e:
        logger.error(f"[SCHEDULER] Error during scheduled tick: {e}")

def start_scheduler():
    if not scheduler.running and settings.SCHEDULER_ENABLED:
        scheduler.add_job(
            tick_job,
            CronTrigger.from_crontab(settings.HOURLY_TICK_CRON),
            id="hourly_autopilot_tick",
            replace_existing=True
        )
        scheduler.start()
        logger.info(f"[SCHEDULER] Scheduler started with cron: {settings.HOURLY_TICK_CRON} ({settings.SCHEDULER_TIMEZONE})")

def pause_scheduler():
    if scheduler.running:
        scheduler.pause()
        logger.info("[SCHEDULER] Scheduler paused.")

def resume_scheduler():
    if scheduler.running:
        scheduler.resume()
        logger.info("[SCHEDULER] Scheduler resumed.")

def get_scheduler_status() -> dict:
    return {
        "running": scheduler.running,
        "state": "RUNNING" if scheduler.running else "STOPPED",
        "jobs": [str(j) for j in scheduler.get_jobs()],
        "timezone": settings.SCHEDULER_TIMEZONE,
        "cron": settings.HOURLY_TICK_CRON
    }
