from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.deals import router as deals_router
from app.api.intelligence import router as intelligence_router
from app.api.outcomes import router as outcomes_router
from app.init_db import init_db

BASE_DIR = Path(__file__).resolve().parent

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="REVORA",
    description="An AI Revenue Memory Engine That Learns From Every Deal.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(deals_router)
app.include_router(intelligence_router)
app.include_router(outcomes_router)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "REVORA", "version": "0.1.0"}

@app.get("/", include_in_schema=False)
async def dashboard():
    return FileResponse(BASE_DIR / "static" / "index.html")
