from app.schemas.Resultado import Resultado
from app.services.solution import get_all

from fastapi import APIRouter


router = APIRouter()


@router.get("/", response_model=list[Resultado], status_code=200)
async def get_results():
    return get_all()