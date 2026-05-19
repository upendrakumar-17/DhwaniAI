import os
import csv
import zipfile
import xml.etree.ElementTree as ET
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pypdf import PdfReader

from app.models.organization_model import Organization
from app.models.organization_file import OrganizationFile

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

BASE_VECTOR_STORE_DIR = "vector_stores/"

def extract_text_from_file(file_path: str) -> str:
    """
    Extract text content from various file types.
    Supports txt, md, pdf, csv, docx.
    """
    if not os.path.exists(file_path):
        return ""

    _, ext = os.path.splitext(file_path.lower())
    
    try:
        if ext in [".txt", ".md"]:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

        elif ext == ".pdf":
            reader = PdfReader(file_path)
            content = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    content.append(text)
            return "\n".join(content)

        elif ext == ".csv":
            content = []
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f)
                for row in reader:
                    content.append(", ".join(row))
            return "\n".join(content)

        elif ext == ".docx":
            # Fallback Docx reader using zipfile XML parser
            try:
                doc = zipfile.ZipFile(file_path)
                xml_content = doc.read('word/document.xml')
                root = ET.fromstring(xml_content)
                namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                text_nodes = root.findall('.//w:t', namespaces)
                return "\n".join([node.text for node in text_nodes if node.text])
            except Exception as docx_err:
                print(f"Error parsing Word file xml fallback: {docx_err}")
                return ""

        else:
            # General fallback: try reading as utf-8 text
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

    except Exception as e:
        print(f"Failed to read file {file_path}: {str(e)}")
        return ""


class VectorStoreService:
    @staticmethod
    def get_embeddings_model():
        """
        Loads the Google Generative AI embeddings model using the GEMINI_API_KEY from environment variables.
        Using model: models/gemini-embedding-2.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="GEMINI_API_KEY is not configured in the environment variables."
            )
        return GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=api_key
        )

    @classmethod
    def build_organization_vector_store(cls, db: Session, organization_id: int):
        """
        Builds a local FAISS vector store index for the organization.
        It parses all files uploaded by the organization, splits them,
        generates embeddings, and stores the index locally.
        """
        # 1. Verify organization exists
        org = db.query(Organization).filter(Organization.id == organization_id).first()
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organization with ID {organization_id} not found."
            )

        # 2. Get all organization files
        files = db.query(OrganizationFile).filter(OrganizationFile.organization_id == organization_id).all()
        if not files:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No files found for organization {org.name}. Please upload files first."
            )

        documents = []
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        processed_files_count = 0

        # 3. Extract text and create Document chunks
        for db_file in files:
            file_path = db_file.file_path
            if not os.path.exists(file_path):
                # Fallback: check if we need to prefix workspace dir
                if not os.path.isabs(file_path) and os.path.exists(os.path.join(os.getcwd(), file_path)):
                    file_path = os.path.join(os.getcwd(), file_path)
                else:
                    continue

            text = extract_text_from_file(file_path)
            if not text or not text.strip():
                continue

            chunks = text_splitter.split_text(text)
            if chunks:
                processed_files_count += 1
                for i, chunk in enumerate(chunks):
                    doc = Document(
                        page_content=chunk,
                        metadata={
                            "organization_id": organization_id,
                            "file_id": db_file.id,
                            "filename": db_file.filename,
                            "chunk_index": i
                        }
                    )
                    documents.append(doc)

        if not documents:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Failed to extract any text content from the uploaded files. Ensure they are text, PDF, CSV, or DOCX files with readable content."
            )

        # 4. Generate FAISS vector store
        try:
            embeddings = cls.get_embeddings_model()
            vector_store = FAISS.from_documents(documents, embeddings)
            
            # Save the index locally to a dedicated organization directory
            org_store_dir = os.path.join(BASE_VECTOR_STORE_DIR, str(organization_id))
            os.makedirs(org_store_dir, exist_ok=True)
            vector_store.save_local(org_store_dir)

            return {
                "message": "Vector store created successfully.",
                "organization_id": organization_id,
                "organization_name": org.name,
                "files_indexed": processed_files_count,
                "total_files": len(files),
                "total_chunks": len(documents)
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error building vector store: {str(e)}"
            )

    @classmethod
    def search_organization_vector_store(cls, db: Session, organization_id: int, query: str, top_k: int = 5):
        """
        Searches the organization's local FAISS vector store.
        """
        # 1. Verify organization exists
        org = db.query(Organization).filter(Organization.id == organization_id).first()
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organization with ID {organization_id} not found."
            )

        # 2. Check if vector store exists
        org_store_dir = os.path.join(BASE_VECTOR_STORE_DIR, str(organization_id))
        index_file = os.path.join(org_store_dir, "index.faiss")
        if not os.path.exists(index_file):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Vector store not created for organization {org.name}. Please trigger the vector store build API first."
            )

        # 3. Perform search
        try:
            embeddings = cls.get_embeddings_model()
            vector_store = FAISS.load_local(org_store_dir, embeddings, allow_dangerous_deserialization=True)
            
            # Search matches with cosine similarity scores (or distances depending on FAISS index)
            results = vector_store.similarity_search_with_score(query, k=top_k)
            
            search_results = []
            for doc, score in results:
                search_results.append({
                    "content": doc.page_content,
                    "score": float(score),
                    "metadata": doc.metadata
                })

            return {
                "organization_id": organization_id,
                "query": query,
                "results": search_results
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error searching vector store: {str(e)}"
            )
