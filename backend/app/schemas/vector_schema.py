from pydantic import BaseModel, Field
from typing import List, Dict, Any

class VectorStoreBuildResponse(BaseModel):
    message: str = Field(..., description="Success message")
    organization_id: int = Field(..., description="The ID of the organization")
    organization_name: str = Field(..., description="The name of the organization")
    files_indexed: int = Field(..., description="Number of files successfully processed and indexed")
    total_files: int = Field(..., description="Total files associated with the organization")
    total_chunks: int = Field(..., description="Total text chunks indexed in the vector store")

    class Config:
        from_attributes = True

class VectorStoreSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The search query text")
    top_k: int = Field(5, ge=1, le=50, description="The number of top matching chunks to retrieve")

class SearchResultItem(BaseModel):
    content: str = Field(..., description="The chunk text content")
    score: float = Field(..., description="The similarity/distance score")
    metadata: Dict[str, Any] = Field(..., description="The metadata associated with the chunk (e.g. filename, file_id)")

class VectorStoreSearchResponse(BaseModel):
    organization_id: int = Field(..., description="The ID of the organization")
    query: str = Field(..., description="The searched query")
    results: List[SearchResultItem] = Field(..., description="List of search results")

    class Config:
        from_attributes = True
