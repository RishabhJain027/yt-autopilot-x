from fastapi import APIRouter, BackgroundTasks
from scheduler.daemon import get_scheduler_status, pause_scheduler, resume_scheduler
from python.pipelines.hourly_tick import hourly_tick
from python.schemas.api_response import ApiResponse

router = APIRouter(prefix='/scheduler', tags=['Scheduler'])

@router.get('/status', response_model=ApiResponse[dict])
async def scheduler_status():
    return ApiResponse(data=get_scheduler_status())

@router.post('/pause', response_model=ApiResponse[dict])
async def scheduler_pause():
    pause_scheduler()
    return ApiResponse(data={'status': 'PAUSED'})

@router.post('/resume', response_model=ApiResponse[dict])
async def scheduler_resume():
    resume_scheduler()
    return ApiResponse(data={'status': 'RESUMED'})

@router.post('/trigger-tick', response_model=ApiResponse[dict])
async def trigger_manual_tick(bg: BackgroundTasks):
    bg.add_task(hourly_tick.run_tick)
    return ApiResponse(data={'status': 'HOURLY_TICK_TRIGGERED'})
