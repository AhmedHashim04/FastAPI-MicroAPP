from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from database import Base, engine

class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("phone", name="uq_users_phone"),)
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, index=True)
    hashed_password = Column(String)

    # حقول خاصة بإعادة التعيين عبر OTP
    otp_hash = Column(String, nullable=True)          
    otp_expires_at = Column(DateTime, nullable=True)   
    otp_purpose = Column(String, nullable=True)       
    otp_last_sent_at = Column(DateTime, nullable=True) 

Base.metadata.create_all(bind=engine)