from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database.connection import engine, Base, test_db_connection
from app.routes.org_routes import router as org_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    # 2. Run the connection test
    test_db_connection()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(org_router)

@app.get("/server")
def server():
    return {
        "message": "Backend Running"
    }
