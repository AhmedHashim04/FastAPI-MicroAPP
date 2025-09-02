import os
from passlib.context import CryptContext
from fastapi.security import APIKeyHeader


SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

api_key_scheme = APIKeyHeader(name="Authorization",description="Get token from login endpoint and pass as--> Bearer <token>")

# from fastapi.security import OAuth2PasswordBearer
# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="/auth/login",
#     scopes={"read": "Read access", "write": "Write access"}
# )
