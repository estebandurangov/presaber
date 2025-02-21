from fastapi import FastAPI
from app.api.router import api_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router, prefix="/api")
    return app

app = create_app()