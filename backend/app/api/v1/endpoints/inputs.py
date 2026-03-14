"""Input ingestion endpoints for fridge, meal, receipt, and chat context."""

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.chat_message import ChatMessage
from app.models.input_job import InputJob
from app.schemas.auth import AuthContext
from app.schemas.contracts import (
    ChatMessageRequest,
    ChatMessageResponse,
    FridgeScanRequest,
    JobEnvelope,
    JobStatus,
    MealScanRequest,
    ReceiptScanRequest,
)
from app.services.input_jobs import process_input_job
from app.services.user_context import ensure_user

router = APIRouter(prefix="/inputs", tags=["inputs"])


def _create_input_job(
    *,
    db: Session,
    user_id: str,
    input_type: str,
    payload: dict,
    background_tasks: BackgroundTasks,
) -> JobEnvelope:
    job = InputJob(user_id=user_id, input_type=input_type, status=JobStatus.PENDING.value, payload=payload)
    db.add(job)
    db.commit()
    db.refresh(job)

    background_tasks.add_task(process_input_job, job.id)

    return JobEnvelope(job_id=job.id, status=JobStatus.PENDING)


@router.post("/fridge-scan", response_model=JobEnvelope, status_code=status.HTTP_202_ACCEPTED)
async def submit_fridge_scan(
    payload: FridgeScanRequest,
    background_tasks: BackgroundTasks,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JobEnvelope:
    ensure_user(db, current_user)
    return _create_input_job(
        db=db,
        user_id=current_user.user_id,
        input_type="fridge_scan",
        payload=payload.model_dump(),
        background_tasks=background_tasks,
    )


@router.post("/meal-scan", response_model=JobEnvelope, status_code=status.HTTP_202_ACCEPTED)
async def submit_meal_scan(
    payload: MealScanRequest,
    background_tasks: BackgroundTasks,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JobEnvelope:
    ensure_user(db, current_user)
    return _create_input_job(
        db=db,
        user_id=current_user.user_id,
        input_type="meal_scan",
        payload=payload.model_dump(),
        background_tasks=background_tasks,
    )


@router.post("/receipt-scan", response_model=JobEnvelope, status_code=status.HTTP_202_ACCEPTED)
async def submit_receipt_scan(
    payload: ReceiptScanRequest,
    background_tasks: BackgroundTasks,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JobEnvelope:
    ensure_user(db, current_user)
    return _create_input_job(
        db=db,
        user_id=current_user.user_id,
        input_type="receipt_scan",
        payload=payload.model_dump(),
        background_tasks=background_tasks,
    )


@router.get("/jobs/{job_id}", response_model=JobEnvelope)
async def get_job_status(
    job_id: str,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JobEnvelope:
    job = db.get(InputJob, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Input job not found")
    if job.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden job scope")

    return JobEnvelope(job_id=job.id, status=JobStatus(job.status), result=job.result)


@router.post("/chat-message", response_model=ChatMessageResponse)
async def submit_chat_message(
    payload: ChatMessageRequest,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ChatMessageResponse:
    ensure_user(db, current_user)

    event = ChatMessage(user_id=current_user.user_id, message=payload.message)
    db.add(event)
    db.commit()
    db.refresh(event)

    return ChatMessageResponse(event_id=event.id, user_id=event.user_id, message=event.message)
