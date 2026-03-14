"""Main API router for version v1."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, feedback, goals, health, inputs, planner, profiles

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(profiles.router)
api_router.include_router(goals.router)
api_router.include_router(inputs.router)
api_router.include_router(planner.router)
api_router.include_router(feedback.router)
