from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.organization_model import Organization
from app.schemas.org_schema import OrganizationCreate, OrganizationResponse, OrganizationLogin, Token
from app.utils.password import hash_password, verify_password
from app.services.jwt_service import create_access_token

router = APIRouter()

@router.post("/register-org", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
def register_organization(org_data: OrganizationCreate, db: Session = Depends(get_db)):
    # Check if organization name already exists
    existing_name = db.query(Organization).filter(Organization.name == org_data.name).first()
    if existing_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An organization with this name already exists."
        )

    # Check if organization email already exists
    existing_email = db.query(Organization).filter(Organization.email == org_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An organization with this email already exists."
        )

    # Hash the password using our password utility function
    hashed_pwd = hash_password(org_data.password)

    # Create new Organization
    new_org = Organization(
        name=org_data.name,
        email=org_data.email,
        password=hashed_pwd
    )

    db.add(new_org)
    db.commit()
    db.refresh(new_org)

    return new_org


@router.post("/login-org", response_model=Token)
def login_organization(login_data: OrganizationLogin, db: Session = Depends(get_db)):
    # Check if organization exists by email
    org = db.query(Organization).filter(Organization.email == login_data.email).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Verify the provided password
    if not verify_password(login_data.password, org.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Generate JWT access token
    access_token = create_access_token(data={"sub": org.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "organization": org
    }

