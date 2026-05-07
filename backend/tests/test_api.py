import sqlite3
import pytest
from pathlib import Path
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.fixture(autouse=True)
def setup_db():
    """确保测试用数据库和表存在"""
    db_path = Path("data/osint.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            query TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            report_path TEXT
        )
    """)
    conn.commit()
    conn.close()
    yield
    # 清理测试数据库
    if db_path.exists():
        db_path.unlink()


@pytest.mark.asyncio
async def test_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_task():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/tasks", json={"query": "test query"})
    assert resp.status_code == 200
    data = resp.json()
    assert "task_id" in data


@pytest.mark.asyncio
async def test_list_tasks():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/tasks")
    assert resp.status_code == 200
