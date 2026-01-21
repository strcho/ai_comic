import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from contextlib import asynccontextmanager
from src.config import get_settings, ensure_directories
from src.utils.logger import logger, get_logger
from src.models import ComicRequest, ComicResponse
from src.services.comic_service import ComicService

app_logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app_logger.info("Starting Comic Generation Agent...")
    ensure_directories()
    yield
    app_logger.info("Shutting down Comic Generation Agent...")


app = FastAPI(
    title="Comic Generation Agent",
    description="Automatic comic generation API with OpenAI integration",
    version="1.0.0",
    lifespan=lifespan,
)

settings = get_settings()
comic_service = ComicService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Comic Generation Agent API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/generate")
async def generate_comic(request: ComicRequest):
    app_logger.info(f"Received generate request: {len(request.text)} characters")
    try:
        output_format = request.format if request.format else "png"
        result = await comic_service.generate_comic(
            text=request.text,
            output_format=output_format,
            output_path=""
        )
        return {"success": True, "data": result}
    except Exception as e:
        app_logger.error(f"Generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/task/{task_id}")
async def get_task(task_id: str):
    try:
        result = comic_service.get_task_status(task_id)
        return {"success": True, "data": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/history")
async def get_history():
    history = comic_service.get_history()
    return {"success": True, "data": history}


@app.get("/api/comic/{task_id}")
async def download_comic(task_id: str):
    try:
        task = comic_service.get_task_status(task_id)
        if task.get("status") != "completed":
            raise HTTPException(status_code=400, detail="Comic not ready")
        
        output_path = task.get("output_path")
        if not output_path or not os.path.exists(output_path):
            raise HTTPException(status_code=404, detail="Comic file not found")
        
        return FileResponse(
            output_path,
            media_type="image/png",
            filename=os.path.basename(output_path)
        )
    except Exception as e:
        app_logger.error(f"Download failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    app_logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )