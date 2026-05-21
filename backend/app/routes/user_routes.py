from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user_model import User
from app.models.organization_model import Organization
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin, UserToken, UserUpdate
from app.utils.password import hash_password, verify_password
from app.services.jwt_service import create_access_token, get_current_user

router = APIRouter(tags=["Users"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user with name, email, password, and organization ID.
    Passwords are automatically and securely hashed.
    """
    # Verify organization exists
    org = db.query(Organization).filter(Organization.id == user_data.org_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Organization with ID {user_data.org_id} does not exist."
        )

    # Check if the user email is already registered
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )

    # Hash the password securely using bcrypt
    hashed_pwd = hash_password(user_data.password)

    # Create new User object
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_pwd,
        org_id=user_data.org_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post(
    "/login",
    response_model=UserToken,
    summary="Log in user and get JWT token"
)
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Log in a user using email and password, returning a secure JWT access token.
    """
    # Check if the user exists
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Verify user password
    if not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is deactivated."
        )

    # Generate JWT token
    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user details"
)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Retrieve details of the currently authenticated user.
    """
    return current_user


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile"
)
def update_me(
    profile_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update profile details (name, email, or password) of the authenticated user.
    """
    # If updating email, check for uniqueness
    if profile_data.email and profile_data.email != current_user.email:
        existing_email = db.query(User).filter(User.email == profile_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email address already exists."
            )
        current_user.email = profile_data.email

    if profile_data.name:
        current_user.name = profile_data.name

    if profile_data.password:
        current_user.password = hash_password(profile_data.password)

    db.commit()
    db.refresh(current_user)

    return current_user
