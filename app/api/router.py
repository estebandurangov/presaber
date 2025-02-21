from fastapi import APIRouter
from app.api.routes import results

api_router = APIRouter()

api_router.include_router(results.router, prefix="/results", tags=["results"])