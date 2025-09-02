from passlib.context import CryptContext
import hashlib
import hmac

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_otp(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()

def consttime_compare(a: str, b: str) -> bool:
    return hmac.compare_digest(a, b)

