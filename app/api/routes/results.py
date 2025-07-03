from app.schemas.Resultado import Resultado
from app.services.solution import get_all, promedios_grupo, promedio_general

from fastapi import APIRouter


router = APIRouter()


@router.get("/", response_model=list[Resultado], status_code=200)
async def get_results(municipio: str = None):
    if municipio:
        df = get_all()
        df_filtrado = df[df["Municipio"] == municipio]
        return df_filtrado.to_dict(orient='records')
    return get_all().to_dict(orient='records')

@router.get("/institucion", response_model=None, status_code=200)
async def get_results_institucion():
    """
    Devuelve el resultado de la institucion
    """
    resultado_estudiantes = get_all()
    return {'grupos': promedios_grupo(resultado_estudiantes),
            'general': promedio_general(resultado_estudiantes),
            'total_estudiantes': len(resultado_estudiantes)
            }
