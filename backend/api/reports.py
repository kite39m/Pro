from pathlib import Path

import aiosqlite
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

router = APIRouter(tags=["reports"])

DB_PATH = Path("data/osint.db")


@router.get("/reports/{task_id}")
async def get_report(task_id: str):
    async with aiosqlite.connect(str(DB_PATH)) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
            row = await cursor.fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail="Task not found")

            report_path = row["report_path"]
            if report_path and Path(report_path).exists():
                content = Path(report_path).read_text(encoding="utf-8")
                return PlainTextResponse(content)

            raise HTTPException(status_code=404, detail="Report not found")


@router.get("/reports")
async def list_reports(limit: int = 20, offset: int = 0):
    async with aiosqlite.connect(str(DB_PATH)) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id, query, status, created_at, completed_at FROM tasks WHERE status = 'completed' ORDER BY completed_at DESC LIMIT ? OFFSET ?",
            (limit, offset),
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
