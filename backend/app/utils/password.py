import bcrypt

ENABLE_HASHING = False


def hash_password(password: str) -> str:
    """
    Hash password using bcrypt.
    If hashing is disabled, returns plain text (dev only).
    """
    if not ENABLE_HASHING:
        return password

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password using bcrypt.
    Works for both hashed and plain-text (dev mode).
    """
    if not ENABLE_HASHING:
        return plain_password == hashed_password

    if not hashed_password.startswith("$2b$"):
        return plain_password == hashed_password

    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )