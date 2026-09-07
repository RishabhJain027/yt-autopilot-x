import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from database.connection import init_db
from scheduler.daemon import start_scheduler
from packages.config.settings import settings
from packages.logger.logger import logger
from apps.api.routes import channels, oauth, topics, productions, analytics, scheduler, system

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('[APP] Initializing database and storage...')
    await init_db()
    if settings.SCHEDULER_ENABLED:
        logger.info('[APP] Starting scheduler daemon...')
        start_scheduler()
    yield
    logger.info('[APP] Shutting down application...')

app = FastAPI(
    title='YT-Autopilot-X API',
    version='1.0.0',
    description='Autonomous YouTube Channel Operating System API',
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

api_v1_prefix = '/api/v1'
app.include_router(channels.router, prefix=api_v1_prefix)
app.include_router(oauth.router, prefix=api_v1_prefix)
app.include_router(topics.router, prefix=api_v1_prefix)
app.include_router(productions.router, prefix=api_v1_prefix)
app.include_router(analytics.router, prefix=api_v1_prefix)
app.include_router(scheduler.router, prefix=api_v1_prefix)
app.include_router(system.router, prefix=api_v1_prefix)

if os.path.exists(settings.STORAGE_ROOT):
    app.mount('/storage', StaticFiles(directory=settings.STORAGE_ROOT), name='storage')

@app.get('/', response_class=HTMLResponse)
async def serve_dashboard():
    dashboard_path = os.path.join('apps', 'dashboard', 'public', 'index.html')
    if os.path.exists(dashboard_path):
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content='<h1>YT-Autopilot-X Control Center</h1><p>API is running.</p>')
