from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.vector_schema import (
    VectorStoreBuildResponse,
    VectorStoreSearchRequest,
    VectorStoreSearchResponse
)
from app.services.vector_store_service import VectorStoreService

router = APIRouter(prefix="/organizations/{organization_id}/vector-store", tags=["Vector Store"])

@router.post(
    "/build",
    response_model=VectorStoreBuildResponse,
    status_code=status.HTTP_200_OK,
    summary="Build or update the organization's vector store index"
)
def build_vector_store(
    organization_id: int,
    db: Session = Depends(get_db)
):
    """
    Parses all documents uploaded by the organization, generates embeddings,
    and builds/updates a local FAISS vector store index.
    """
    return VectorStoreService.build_organization_vector_store(db=db, organization_id=organization_id)

@router.post(
    "/search",
    response_model=VectorStoreSearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Search the organization's vector store"
)
def search_vector_store(
    organization_id: int,
    request: VectorStoreSearchRequest,
    db: Session = Depends(get_db)
):
    """
    Performs similarity search over the organization's indexed documents
    using cosine similarity on FAISS.
    """
    return VectorStoreService.search_organization_vector_store(
        db=db,
        organization_id=organization_id,
        query=request.query,
        top_k=request.top_k
    )
