from app.schemas.Resultado import Resultado
from app.services.solution import get_all
from app.services.institucion import promedios_grupo, promedio_general, get_all_means

from fastapi import APIRouter


router = APIRouter()


@router.get("/", response_model=list[Resultado], status_code=200)
async def get_results(municipio: str = None, institucion: str = None):
    if municipio:
        df = get_all()
        df_filtrado = df[df["Municipio"] == municipio]
        return df_filtrado.to_dict(orient='records')
    if institucion:
        df = get_all()
        df_filtrado = df[df["Institucion"] == institucion]
        df_filtrado = df_filtrado.sort_values(by="codigo")
        return df_filtrado.to_dict(orient='records')
    return get_all().to_dict(orient='records')

@router.get("/institucion", response_model=None, status_code=200)
async def get_results_institucion(institucion: str = None):
    """
    Devuelve el resultado de la institucion
    """
    if not institucion:
        raise ValueError("El parametro institucion es requerido")
    resultado_estudiantes = get_all()
    resultado_estudiantes_filtrado = resultado_estudiantes[resultado_estudiantes["Institucion"] == institucion]
    
    return {'grupos': promedios_grupo(resultado_estudiantes_filtrado),
            'general': promedio_general(resultado_estudiantes_filtrado),
            'medias': get_all_means(resultado_estudiantes_filtrado),
            'total_estudiantes': len(resultado_estudiantes_filtrado)
            }
