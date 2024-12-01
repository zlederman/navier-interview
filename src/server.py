import concurrent.futures as cf
from contextlib import asynccontextmanager
import uuid
from fastapi import FastAPI, APIRouter, HTTPException, Depends
import asyncio 
from typing import Dict

from src.models import ConfigModel, TaskResponse, TaskStatusResponse, PipelineStates
from src.pipeline.run import run_pipeline

active_tasks: Dict[str, asyncio.Task] = {}
states: Dict[str, PipelineStates] = {}

thread_pool = cf.ThreadPoolExecutor(max_workers=3)

router = APIRouter(prefix="/api", tags=["pipeline"])

async def check_if_task_valid(task_id: str):
    if not task_id in states:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found: {task_id}"
        )
    return task_id


@router.post("/trigger-pipeline", response_model=TaskResponse)
async def trigger_pipeline(config: ConfigModel):
    # create new task and start pipeline
    task_id = str(uuid.uuid4())
    active_tasks[task_id] = asyncio.create_task(run_pipeline(config, task_id, states, thread_pool))

    return TaskResponse(task_id=task_id)

@router.get('/status/{task_id}', response_model=TaskStatusResponse)
async def get_status(task_id: str = Depends(check_if_task_valid)):
    if not task_id in states:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found: {task_id}"
        )
    
    state = states[task_id]
    return TaskStatusResponse(task_id=task_id, status=state)


@router.post('/stop-pipeline/{task_id}', response_model=TaskStatusResponse)
async def stop_pipeline(task_id: str = Depends(check_if_task_valid)):
    current_task = active_tasks[task_id]
    current_task.cancel()

    del states[task_id]
    del active_tasks[task_id]

    return TaskStatusResponse(task_id, status=PipelineStates.CANCELLED)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    thread_pool.shutdown(wait=False)
    for task in active_tasks.values():
        if not task.done():
            task.cancel()
            
def create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    
    return app