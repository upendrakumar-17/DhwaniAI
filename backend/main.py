from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database.base import Base
from app.database.connection import engine, test_db_connection
from app.routes.org_routes import router as org_router
from app.routes.file_routes import router as file_router
from app.routes.vector_routes import router as vector_router
from app.routes.chat_routes import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    # 2. Run the connection test
    test_db_connection()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(org_router)
app.include_router(file_router)
app.include_router(vector_router)
app.include_router(chat_router)

@app.get("/")
def server():
    return {
        "message": "Backend Running"
    }
