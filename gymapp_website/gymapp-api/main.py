import time
import atexit
from uuid import uuid4
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

from fastapi import FastAPI, Request, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from routers import users, exercises, workouts, planned_workouts, analysis
from utils.db import init_db, get_session, engine
from migrations.json_sync import import_all_data, export_all_data
from models.users import UsersDB


load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    print("Warning: ANTHROPIC_API_KEY not found in environment variables")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    print("Starting up...")
    
    init_db()
    
    with Session(engine) as session:
        import_all_data(session)
    
    yield
    
    print("Shutting down...")
    
    with Session(engine) as session:
        export_all_data(session)


app = FastAPI(
    title="Gym API",
    description="Gym Management API",
    version="1.0.0",
    lifespan=lifespan
)

def cleanup():
    """Cleanup function for unexpected shutdowns"""
    try:
        with Session(engine) as session:
            export_all_data(session)
    except Exception as e:
        print(f"Error during cleanup: {e}")

atexit.register(cleanup)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router)
app.include_router(users.router)
app.include_router(exercises.router)
app.include_router(workouts.router)
app.include_router(planned_workouts.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    rid = uuid4()
    start_time = time.time()

    response = await call_next(request)

    process_time = int((time.time() - start_time) * 1000)
    
    print(f"Request {rid}: {request.method} {request.url.path} - {response.status_code} - {process_time}ms")

    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Log validation errors"""
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    print(f"Unhandled exception: {str(exc)}")
    content = {"status_code": 500, "message": "Internal server error", "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@app.get("/health", tags=["Health"])
async def health_check(session: Session = Depends(get_session)):
    """Health check endpoint"""
    try:
        statement = select(UsersDB).limit(1)
        session.exec(statement)
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "timestamp": time.time()
    }


@app.post("/admin/import", tags=["Admin"])
async def manual_import(session: Session = Depends(get_session)):
    """Manually trigger data import from JSON"""
    try:
        import_all_data(session)
        return {"status": "success", "message": "Data imported successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/admin/export", tags=["Admin"])
async def manual_export(session: Session = Depends(get_session)):
    """Manually trigger data export to JSON"""
    try:
        export_all_data(session)
        return {"status": "success", "message": "Data exported successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7778)