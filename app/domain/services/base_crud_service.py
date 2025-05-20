from __future__ import annotations
from typing import Any, Generic, TypeVar
from uuid import UUID
from datetime import date
from app.domain.ports.base_crud_repository import BaseCRUDRepository
from app.errors.service import ServiceUnavailableException

ModelType = TypeVar("ModelType")
CrudType = TypeVar("CrudType", bound=BaseCRUDRepository)

class BaseService(Generic[ModelType, CrudType]):
    def __init__(self) -> None:
        self.observer: CrudType | None = None

    def register_observer(self, observer: CrudType) -> None:
        self.observer = observer

    def unregister_observer(self) -> None:
        self.observer = None

    def get_by_id(self, id: UUID, db: Any) -> ModelType:
        if self.observer is None:
            raise ServiceUnavailableException()
        return self.observer.get_by_id(id, db)

    def get_multi(self, db: Any) -> list[ModelType]:
        if self.observer is None:
            raise ServiceUnavailableException()
        return self.observer.get_multi(db)

    def create(self, obj_in: Any, db: Any) -> ModelType:
        if self.observer is None:
            raise ServiceUnavailableException()
        return self.observer.create(obj_in, db)

    def delete(self, id: UUID, db: Any) -> int:
        if self.observer is None:
            raise ServiceUnavailableException()
        return self.observer.delete(id, db)
