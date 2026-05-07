import asyncio
import json
import uuid
from datetime import datetime
from pathlib import Path

import aiosqlite
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

from agents.graph import get_graph
from config import get_settings

router = APIRouter(tags=["tasks"])

DB_PATH = Path("data/osint.db")
OUTPUT_DIR = Path("output")

task_events: dict[str, list[dict]] = {}


class TaskCreate(BaseModel):
    query: str


class TaskResponse(BaseModel):
    task_id: str
    query: str
    status: str
    created_at: str


@router.post("/tasks", response_model=dict)
async def create_task(body: TaskCreate, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())

    async with aiosqlite.connect(str(DB_PATH)) as db:
        await db.execute(
            "INSERT INTO tasks (id, query, status) VALUES (?, ?, ?)",
            (task_id, body.query, "running"),
        )
        await db.commit()

    task_events[task_id] = []
    background_tasks.add_task(run_agent_workflow, task_id, body.query)

    return {"task_id": task_id}


@router.get("/tasks/{task_id}")
async def get_task(task_id: str):
    async with aiosqlite.connect(str(DB_PATH)) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return {"error": "Task not found"}, 404
            return dict(row)


@router.get("/tasks")
async def list_tasks(limit: int = 20, offset: int = 0):
    async with aiosqlite.connect(str(DB_PATH)) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM tasks ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset),
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def run_agent_workflow(task_id: str, query: str):
    """后台执行 Agent 工作流"""
    graph = get_graph()

    initial_state = {
        "user_query": query,
        "sub_tasks": [],
        "raw_findings": [],
        "insights": [],
        "draft_report": "",
        "critique": "",
        "needs_revision": False,
        "revision_queries": [],
        "final_report": "",
        "sources": [],
        "status": "pending",
    }

    config = {"configurable": {"thread_id": task_id}}

    try:
        events = []
        async for event in graph.astream(initial_state, config=config):
            for node, output in event.items():
                status = output.get("status", node)
                evt = {"agent": node, "status": status, "timestamp": datetime.now().isoformat()}
                events.append(evt)
                if task_id in task_events:
                    task_events[task_id].append(evt)

        final_state = await graph.aget_state(config)
        final_report = final_state.values.get("final_report", "")

        report_dir = OUTPUT_DIR / task_id
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / "report.md"
        report_path.write_text(final_report, encoding="utf-8")

        raw_path = report_dir / "raw_findings.json"
        raw_path.write_text(
            json.dumps(final_state.values.get("raw_findings", []), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        async with aiosqlite.connect(str(DB_PATH)) as db:
            await db.execute(
                "UPDATE tasks SET status = ?, completed_at = ?, report_path = ? WHERE id = ?",
                ("completed", datetime.now().isoformat(), str(report_path), task_id),
            )
            await db.commit()

        if task_id in task_events:
            task_events[task_id].append({
                "agent": "system",
                "status": "completed",
                "report_path": str(report_path),
                "timestamp": datetime.now().isoformat(),
            })

    except Exception as e:
        async with aiosqlite.connect(str(DB_PATH)) as db:
            await db.execute(
                "UPDATE tasks SET status = ? WHERE id = ?",
                ("failed", task_id),
            )
            await db.commit()

        if task_id in task_events:
            task_events[task_id].append({
                "agent": "system",
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            })
