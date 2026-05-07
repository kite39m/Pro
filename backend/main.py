import asyncio
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

import aiosqlite
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.tasks import router as tasks_router
from api.reports import router as reports_router
from api.stream import router as stream_router


DB_PATH = Path("data/osint.db")
OUTPUT_DIR = Path("output")


@asynccontextmanager
async def lifespan(app: FastAPI):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    async with aiosqlite.connect(str(DB_PATH)) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                query TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                report_path TEXT
            )
        """)
        await db.commit()

    yield


app = FastAPI(title="OSINT Engine", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_router, prefix="/api")
app.include_router(reports_router, prefix="/api")
app.include_router(stream_router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}
