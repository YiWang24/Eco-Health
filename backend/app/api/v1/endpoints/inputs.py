"""Input ingestion endpoints for fridge, meal, receipt, and chat context."""

from uuid import uuid4

from fastapi import APIRouter

from app.schemas.contracts import JobEnvelope, JobStatus

router = APIRouter(prefix="/inputs", tags=["inputs"])


@router.post("/fridge-scan", response_model=JobEnvelope)
async def submit_fridge_scan() -> JobEnvelope:
    return JobEnvelope(job_id=str(uuid4()), status=JobStatus.PENDING)


@router.post("/meal-scan", response_model=JobEnvelope)
async def submit_meal_scan() -> JobEnvelope:
    return JobEnvelope(job_id=str(uuid4()), status=JobStatus.PENDING)


@router.post("/receipt-scan", response_model=JobEnvelope)
async def submit_receipt_scan() -> JobEnvelope:
    return JobEnvelope(job_id=str(uuid4()), status=JobStatus.PENDING)


@router.post("/chat-message")
async def submit_chat_message() -> dict[str, str]:
    return {"status": "stub", "message": "Chat-context ingestion is not implemented yet."}
