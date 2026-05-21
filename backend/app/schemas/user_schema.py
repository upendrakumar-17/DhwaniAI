from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="The full name of the user")
    email: str = Field(..., min_length=5, max_length=150, description="The email address of the user")
    password: str = Field(..., min_length=1, max_length=100, description="The password for the user account (minimum 6 characters)")
    org_id: int = Field(..., description="The ID of the organization the user belongs to")


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    org_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Update the user's name")
    email: Optional[str] = Field(None, min_length=5, max_length=150, description="Update the user's email")
    password: Optional[str] = Field(None, min_length=1, max_length=100, description="Update the user's password")


class UserLogin(BaseModel):
    email: str = Field(..., description="The email address of the user")
    password: str = Field(..., description="The password for the user account")


class UserToken(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
