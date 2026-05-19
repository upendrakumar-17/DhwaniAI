# app/utils/file_upload.py

import os
from fastapi import UploadFile


BASE_UPLOAD_DIR = "uploads/"


def save_organization_file(
    organization_id: int,
    file: UploadFile
):
    org_folder = os.path.join(
        BASE_UPLOAD_DIR,
        str(organization_id)
    )

    os.makedirs(org_folder, exist_ok=True)

    file_path = os.path.join(
        org_folder,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return {
        "filename": file.filename,
        "file_path": file_path,
    }