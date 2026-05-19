from pydantic import BaseModel, Field

class OrganizationCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="The name of the organization")
    email: str = Field(..., min_length=5, max_length=150, description="The contact email address of the organization")
    password: str = Field(..., min_length=6, max_length=100, description="The password for the organization account")

class OrganizationResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True

class OrganizationLogin(BaseModel):
    email: str = Field(..., description="The contact email address of the organization")
    password: str = Field(..., description="The password for the organization account")

class Token(BaseModel):
    access_token: str
    token_type: str
    organization: OrganizationResponse

