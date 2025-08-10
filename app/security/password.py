from passlib.context import CryptContext

# Create password context using Argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate a password hash using Argon2."""
    return pwd_context.hash(password) 