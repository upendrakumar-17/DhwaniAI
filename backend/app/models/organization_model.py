from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database.connection import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    email = Column(String(150), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)  # Hashed password
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}', email='{self.email}')>"
