from .base import BaseErrors

class ServiceUnavailableException(BaseErrors):
    def __init__(self):
        super().__init__(code=503, detail="Service Unavailable")