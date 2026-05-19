from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.models.organization_model import Organization
from app.models.organization_file import OrganizationFile
from app.schemas.file_schema import FileResponse
from app.utils.file_upload import save_organization_file

router = APIRouter(tags=["Files"])


@router.post("/upload-file", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
def upload_file(
    organization_id: int = Form(..., description="The ID of the organization uploading the file"),
    file: UploadFile = File(..., description="The file to be uploaded"),
    db: Session = Depends(get_db)
):
    # 1. Verify organization exists
    org = db.query(Organization).filter(Organization.id == organization_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with ID {organization_id} not found."
        )

    # 2. Save physical file to storage
    try:
        saved_info = save_organization_file(organization_id=organization_id, file=file)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )

    # 3. Save file metadata to database
    db_file = OrganizationFile(
        organization_id=organization_id,
        filename=saved_info["filename"],
        file_path=saved_info["file_path"]
    )
    
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return db_file


@router.get("/organizations/{organization_id}/files", response_model=List[FileResponse])
def get_organization_files(
    organization_id: int,
    db: Session = Depends(get_db)
):
    # Verify organization exists
    org = db.query(Organization).filter(Organization.id == organization_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with ID {organization_id} not found."
        )

    return org.files
