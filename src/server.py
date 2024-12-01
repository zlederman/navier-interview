import concurrent.futures as cf
from contextlib import asynccontextmanager
import uuid
from fastapi import FastAPI, APIRouter, HTTPException
import asyncio 

from src.models import ConfigModel, TaskResponse, TaskStatusResponse
from src.pipeline.run import run_pipeline

tasks = {}
states = {}
thread_pool = cf.ThreadPoolExecutor(max_workers=3)

router = APIRouter(prefix="/api", tags=["pipeline"])

@router.post("/trigger", response_model=TaskResponse)
async def trigger_pipeline(config: ConfigModel):
    # create new task and start pipeline
    task_id = str(uuid.uuid4())
    tasks[task_id] = asyncio.create_task(run_pipeline(config, task_id, states, thread_pool))

    return TaskResponse(task_id=task_id)

@router.get('/status/{task_id}', response_model=TaskStatusResponse)
async def get_status(task_id: str):
    if not task_id in states:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found: {task_id}"
        )
    
    state = states[task_id]
    return TaskStatusResponse(task_id=task_id, status=state)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    thread_pool.shutdown(wait=False)
    for task in tasks.values():
        if not task.done():
            task.cancel()
            
def create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    
    
    async def shutdown_event():
        thread_pool.shutdown(wait=False)
    return app