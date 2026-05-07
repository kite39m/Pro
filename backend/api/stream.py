import asyncio
import json

from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

from api.tasks import task_events

router = APIRouter(tags=["stream"])


@router.get("/tasks/{task_id}/stream")
async def stream_task(task_id: str):
    """SSE 实时推送任务进度"""

    async def event_generator():
        last_index = 0
        while True:
            events = task_events.get(task_id, [])
            if len(events) > last_index:
                for event in events[last_index:]:
                    yield {
                        "event": f"agent_{event.get('status', 'progress')}",
                        "data": json.dumps(event, ensure_ascii=False),
                    }
                last_index = len(events)

                if events and events[-1].get("status") in ("completed", "failed"):
                    break

            await asyncio.sleep(0.5)

    return EventSourceResponse(event_generator())
