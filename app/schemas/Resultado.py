from pydantic import BaseModel

class Resultado(BaseModel):
    Nombre: str
    Grupo: str
    codigo: int
    ciencias_naturales: int 
    matematicas: int
    ciencias_sociales: int
    ingles: int
    comprension_lectora: int
    total: int
    percentil: int
    puesto: int