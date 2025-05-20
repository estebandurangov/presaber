from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

T = TypeVar("T")  # Entidad

class BaseCRUDRepository(ABC, Generic[T]):
    @abstractmethod
    def get_by_id(self, id: UUID) -> T: ...

    @abstractmethod
    def get_multi(self) -> list[T]: ...

    @abstractmethod
    def create(self, obj: T) -> T: ...

    @abstractmethod
    def update(self, id:UUID, obj: T) -> T: ...

    @abstractmethod
    def delete(self, id: UUID) -> None: ...
