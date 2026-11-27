from fastapi import APIRouter

from app.api.v1 import assessments, auth, consultations, health, plans, profile

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(profile.router)
api_router.include_router(assessments.router)
api_router.include_router(plans.router)
api_router.include_router(consultations.router)
