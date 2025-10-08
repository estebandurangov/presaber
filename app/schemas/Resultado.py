from typing import Optional
from pydantic import BaseModel

class Resultado(BaseModel):
    Nombre: str
    Institucion: str
    Grupo: Optional[str] = None
    Documento: Optional[str] = None
    Municipio: Optional[str] = None
    codigo: int
    ciencias_naturales: int 
    matematicas: int
    ciencias_sociales: int
    ingles: int
    lectura_critica: int
    total: int
    percentil: int
    puesto: int