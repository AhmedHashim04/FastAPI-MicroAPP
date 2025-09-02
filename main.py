from fastapi import FastAPI, Depends, HTTPException
from serializers import UserCreate, UserOut, TokenOut, LoginIn, ChangePasswordIn, RequestResetIn, VerifyResetIn, OTPOut
from database import get_db
from sqlalchemy.orm import Session
from security import hash_password
from models.user import User
from utils import get_current_user, create_access_token, send_sms_stub
from security import verify_password, hash_otp, consttime_compare

from datetime import datetime, timedelta
import secrets

app = FastAPI(title="Auth + JWT + OTP ")

@app.post("/auth/register", response_model=UserOut, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.phone == user.phone).first():
        raise HTTPException(status_code=400, detail="Phone already registered")
    db_user = User(phone=user.phone, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/auth/login", response_model=TokenOut)
def login(user: LoginIn, db: Session = Depends(get_db)):
    """
    Authenticate a user using their phone number and password.
    Args:
        user (LoginIn): The login credentials containing phone and password.
        db (Session, optional): SQLAlchemy database session dependency.
    Returns:
        TokenOut: An object containing the generated access token.
        you should store this token securely (e.g., in an HTTP-only cookie).
        and include it in the Authorization header for subsequent requests.
    Raises:
        HTTPException: If the phone number or password is invalid.
    """

    user_db = db.query(User).filter(User.phone == user.phone).first()
    if not user_db or not verify_password(user.password, user_db.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid phone or password")
    token = create_access_token(sub=user_db.phone)
    return TokenOut(access_token=token)

@app.post("/auth/change-password", status_code=204)
def change_password(user: ChangePasswordIn, current: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(user.old_password, current.hashed_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    current.hashed_password = hash_password(user.new_password)
    db.add(current)
    db.commit()
    return


OTP_TTL_SECONDS = 5 * 60   
OTP_RESEND_COOLDOWN = 1

@app.post("/auth/request-reset", status_code=200, response_model=OTPOut)
def request_reset(user: RequestResetIn, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.phone == user.phone).first()
    if not user_db:
        raise HTTPException(status_code=400, detail="If the phone is registered, a code has been sent!")

    now = datetime.now()
    if user_db.otp_last_sent_at and (now - user_db.otp_last_sent_at).total_seconds() < OTP_RESEND_COOLDOWN:
        raise HTTPException(status_code=429, detail="Please wait before requesting another code")

    raw_otp = ''.join(secrets.choice('0123456789') for _ in range(6))
    user_db.otp_hash = hash_otp(raw_otp)
    user_db.otp_expires_at = now + timedelta(seconds=OTP_TTL_SECONDS)
    user_db.otp_purpose = "reset"
    user_db.otp_last_sent_at = now
    db.add(user_db)
    db.commit()

    send_sms_stub(user_db.phone, f"Your reset code is: {raw_otp}. It expires in {OTP_TTL_SECONDS // 60} minutes.")
    return OTPOut(otp=raw_otp)

@app.post("/auth/verify-reset", status_code=204)
def verify_reset(user: VerifyResetIn, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.phone == user.phone).first()
    if not user_db or not user_db.otp_hash or user_db.otp_purpose != "reset":
        raise HTTPException(status_code=400, detail="Invalid code or phone")

    if not user_db.otp_expires_at or datetime.now() > user_db.otp_expires_at:
        user_db.otp_hash = None
        user_db.otp_expires_at = None
        user_db.otp_purpose = None
        db.add(user_db); db.commit()
        raise HTTPException(status_code=400, detail="Code expired")

    if not consttime_compare(user_db.otp_hash, hash_otp(user.otp)):
        raise HTTPException(status_code=400, detail="Invalid code")

    user_db.hashed_password = hash_password(user.new_password)
    user_db.otp_hash = None
    user_db.otp_expires_at = None
    user_db.otp_purpose = None
    db.add(user_db)
    db.commit()
    return

@app.get("/auth/me", response_model=UserOut)
def read_me(current: User = Depends(get_current_user)):
    return current

