from pydantic import BaseModel

class Resultado(BaseModel):
    Nombre: str
    Documento: str
    Institucion: str
    Municipio: str
    codigo: int
    ciencias_naturales: int 
    matematicas: int
    ciencias_sociales: int
    ingles: int
    comprension_lectora: int
    total: int
    percentil: int
    puesto: int