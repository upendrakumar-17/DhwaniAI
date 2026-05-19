from pydantic import BaseModel

class FileResponse(BaseModel):
    id: int
    organization_id: int
    filename: str
    file_path: str

    class Config:
        from_attributes = True
