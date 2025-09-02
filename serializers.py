from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    phone: str = Field(..., example="01012345678", description="Phone number (11 digits)")
    password: str = Field(..., min_length=6, example="strongPass123", description="Password (min 6 characters)")


class TokenOut(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(default="bearer", example="bearer")

class OTPOut(BaseModel):
    otp: str = Field(..., example="123456", description="One-time password (OTP))(this appear here for test only)")

class UserOut(BaseModel):
    id: int = Field(..., example=1)
    phone: str = Field(..., example="01012345678")

    class Config:
        from_attributes = True 


class LoginIn(BaseModel):
    phone: str = Field(..., example="01012345678")
    password: str = Field(..., example="mypassword")


class ChangePasswordIn(BaseModel):
    old_password: str = Field(..., example="oldPass123")
    new_password: str = Field(..., min_length=6, example="newPass456")


class RequestResetIn(BaseModel):
    phone: str = Field(..., example="01012345678")


class VerifyResetIn(BaseModel):
    phone: str = Field(..., example="01012345678")
    otp: str = Field(..., example="123456", description="OTP code sent via SMS")
    new_password: str = Field(..., min_length=6, example="newPass456")
