
from datetime import datetime, timedelta
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, api_key_scheme
from database import get_db
from typing import Optional
from fastapi import  Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from models.user import User


def create_access_token(sub: str, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode = {"sub": sub, "exp": datetime.now() + timedelta(minutes=expires_minutes)}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(db: Session = Depends(get_db), token: str = Depends(api_key_scheme)) -> User:
    credentials_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: Optional[str] = payload.get("sub")
        if sub is None:
            raise credentials_exc
    except JWTError:
        raise credentials_exc
    user = db.query(User).filter(User.phone == sub).first()
    if not user :#or not user.is_active:
        raise credentials_exc
    return user



def send_sms_stub(phone: str, message: str) -> None:
    #(Twilio, Vonage) Soon
    print(f"[SMS] to {phone}: {message}")