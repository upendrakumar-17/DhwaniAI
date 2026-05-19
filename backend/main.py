from fastapi import FastAPI

from app.database.connection import Base
from app.database.connection import engine
from app.database.connection import test_db_connection

# from app.models.organization_model import Organization
# from app.models.user_model import User

app = FastAPI()


@app.on_event("startup")
def startup_event():

    # Test database connection
    test_db_connection()

    # Create tables
    # Base.metadata.create_all(bind=engine)

    # print("✅ Tables created successfully")


@app.get("/")
def home():
    return {
        "message": "Backend Running"
    }