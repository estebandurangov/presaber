from uuid import UUID
from datetime import datetime

class BaseEntity:
    def __init__(self, id: UUID, created_at: datetime = None, updated_at: datetime = None):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
