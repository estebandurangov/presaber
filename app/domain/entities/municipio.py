from uuid import UUID
from app.domain.entities.base_entity import BaseEntity


class Municipio(BaseEntity):
    def __init__(self, id: UUID, nombre: str, created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)
        self.id = id
        self.nombre = nombre