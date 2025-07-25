from fastapi import FastAPI

from app.config.config import settings
from app.database.session import init_db
from app.routers.routes import router

app = FastAPI(title="Async Media Generator")


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(router)
