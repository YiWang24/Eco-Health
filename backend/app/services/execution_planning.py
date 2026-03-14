"""Execution planning helpers for calendar sync, DAG, and proactive prep."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.calendar_block import CalendarBlock as CalendarBlockModel
from app.models.cooking_task import CookingTask
from app.models.prep_window import PrepWindow
from app.schemas.contracts import CalendarBlock, CookingDagTask, ExecutionPlanBlock, ProactivePrepWindow

_CRITICAL_KEYWORDS = {"marinate", "soak", "slow", "bake", "roast", "boil"}


def _estimate_duration_minutes(step: str) -> int:
    lowered = step.lower()
    if any(token in lowered for token in ("marinate", "soak")):
        return 20
    if any(token in lowered for token in ("preheat", "oven")):
        return 10
    if any(token in lowered for token in ("chop", "slice", "prep")):
        return 8
    if any(token in lowered for token in ("cook", "fry", "bake", "boil", "stir")):
        return 15
    if "serve" in lowered:
        return 5
    return 10


def build_cooking_dag_tasks(steps: list[str]) -> list[CookingDagTask]:
    """Build a deterministic DAG from recipe steps."""

    if not steps:
        steps = ["Prepare ingredients", "Cook the meal", "Serve"]

    tasks: list[CookingDagTask] = []
    for index, step in enumerate(steps):
        task_id = f"task-{index + 1}"
        depends_on = [tasks[-1].task_id] if tasks else []
        lowered = step.lower()
        is_critical = any(keyword in lowered for keyword in _CRITICAL_KEYWORDS)
        tasks.append(
            CookingDagTask(
                task_id=task_id,
                title=step.strip() or f"Step {index + 1}",
                duration_minutes=_estimate_duration_minutes(step),
                depends_on=depends_on,
                is_critical_path=is_critical,
            )
        )
    if tasks and not any(task.is_critical_path for task in tasks):
        tasks[0].is_critical_path = True
    return tasks


def build_proactive_prep_windows(
    tasks: list[CookingDagTask],
    *,
    anchor: datetime | None = None,
) -> list[ProactivePrepWindow]:
    """Allocate 5-10 minute proactive prep windows for short tasks."""

    now = anchor or datetime.now(timezone.utc)
    prep_candidates = [task for task in tasks if task.duration_minutes <= 10][:3]
    windows: list[ProactivePrepWindow] = []
    for idx, task in enumerate(prep_candidates):
        start_at = now + timedelta(minutes=10 + idx * 15)
        end_at = start_at + timedelta(minutes=min(10, max(5, task.duration_minutes)))
        windows.append(
            ProactivePrepWindow(
                window_id=f"prep-window-{idx + 1}",
                start_at=start_at,
                end_at=end_at,
                assigned_task_ids=[task.task_id],
                note="Auto-scheduled micro-prep window",
            )
        )
    return windows


def persist_execution_plan(
    *,
    db: Session,
    user_id: str,
    recommendation_id: str,
    recipe_title: str,
    tasks: list[CookingDagTask],
    prep_windows: list[ProactivePrepWindow],
) -> ExecutionPlanBlock:
    """Persist execution artifacts and return API-ready execution plan."""

    now = datetime.now(timezone.utc)
    critical_minutes = sum(task.duration_minutes for task in tasks if task.is_critical_path)
    total_minutes = max(30, critical_minutes)
    calendar_row = CalendarBlockModel(
        user_id=user_id,
        recommendation_id=recommendation_id,
        title=f"Cook: {recipe_title}",
        start_at=now + timedelta(minutes=30),
        end_at=now + timedelta(minutes=30 + total_minutes),
        status="scheduled",
    )
    db.add(calendar_row)
    db.flush()

    persisted_tasks: list[CookingDagTask] = []
    for task in tasks:
        row = CookingTask(
            user_id=user_id,
            recommendation_id=recommendation_id,
            task_type="dag",
            task_key=task.task_id,
            title=task.title,
            duration_minutes=task.duration_minutes,
            depends_on=task.depends_on,
            is_critical_path=task.is_critical_path,
        )
        db.add(row)
        persisted_tasks.append(task)

    persisted_windows: list[ProactivePrepWindow] = []
    for window in prep_windows:
        row = PrepWindow(
            user_id=user_id,
            recommendation_id=recommendation_id,
            start_at=window.start_at,
            end_at=window.end_at,
            assigned_task_ids=window.assigned_task_ids,
            note=window.note,
        )
        db.add(row)
        db.flush()
        persisted_windows.append(
            ProactivePrepWindow(
                window_id=row.id,
                start_at=row.start_at,
                end_at=row.end_at,
                assigned_task_ids=row.assigned_task_ids or [],
                note=row.note,
            )
        )
        for task_id in window.assigned_task_ids:
            prep_task_row = CookingTask(
                user_id=user_id,
                recommendation_id=recommendation_id,
                task_type="prep",
                task_key=f"prep-{task_id}-{uuid4().hex[:6]}",
                title=f"Prep for {task_id}",
                duration_minutes=max(5, min(10, next((t.duration_minutes for t in tasks if t.task_id == task_id), 8))),
                depends_on=[],
                is_critical_path=False,
                scheduled_start=window.start_at,
                scheduled_end=window.end_at,
            )
            db.add(prep_task_row)

    return ExecutionPlanBlock(
        calendar_blocks=[
            CalendarBlock(
                block_id=calendar_row.id,
                title=calendar_row.title,
                start_at=calendar_row.start_at,
                end_at=calendar_row.end_at,
                status=calendar_row.status,
            )
        ],
        cooking_dag_tasks=persisted_tasks,
        proactive_prep_windows=persisted_windows,
    )
