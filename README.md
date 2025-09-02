# 📌 FastAPI Authentication System (JWT + OTP)

A complete authentication system built with **FastAPI + SQLAlchemy** that supports:

- **User Registration** (with phone + password)  
- **Login** with phone + password  
- **Password change** (for logged-in users)  
- **Password reset with OTP** (request OTP, verify OTP, reset password)  
- **JWT-based authentication**  
- **SMS OTP Stub** (can be replaced with Twilio / Vonage / other providers)  

---

## ⚙️ Requirements

- Python 3.10+  
- FastAPI  
- Uvicorn  
- SQLAlchemy  
- Passlib  
- python-jose  

Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose
```

---

## 📂 Project Structure

```
.
├── main.py             # API endpoints
├── database.py         # Database setup
├── models/
│   └── user.py         # User model (SQLAlchemy)
├── security.py         # Password & OTP hashing
├── utils.py            # JWT helpers + SMS Stub
├── serializers.py      # Pydantic Schemas
├── settings.py         # App settings (SECRET_KEY, JWT config)
└── README.md           # This file
```

---

## 🛠️ Configuration

### 1. Database
By default, the app uses **SQLite**:

```python
DATABASE_URL = "sqlite:///./test.db"
```

You can switch to PostgreSQL or MySQL in `database.py`:

```python
# PostgreSQL
DATABASE_URL = "postgresql+psycopg2://user:pass@localhost/dbname"

# MySQL
DATABASE_URL = "mysql+pymysql://user:pass@localhost/dbname"
```

### 2. Secret Key
Update your secret key in `settings.py`:

```python
SECRET_KEY = "CHANGE_ME_TO_A_STRONG_KEY"
```

---

## 🚀 Run the Project

Start the server with:

```bash
uvicorn main:app --reload
```

Open in your browser:

```
http://127.0.0.1:8000/docs
```

This will show the **Swagger UI** where you can test all endpoints.

---

## 📑 API Endpoints

### 🔹 Register a new user
`POST /auth/register`

```json
{
  "phone": "01012345678",
  "password": "mypassword"
}
```

**Response:**
```json
{
  "id": 1,
  "phone": "01012345678"
}
```

---

### 🔹 Login
`POST /auth/login`

```json
{
  "phone": "01012345678",
  "password": "mypassword"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer"
}
```

Use this token in the **Authorization header**:

```
Authorization: Bearer <token>
```

---

### 🔹 Get current user
`GET /auth/me`

Requires the token in the header:

```
Authorization: Bearer <token>
```

---

### 🔹 Change password
`POST /auth/change-password`

```json
{
  "old_password": "mypassword",
  "new_password": "newPass123"
}
```

---

### 🔹 Request password reset (OTP)
`POST /auth/request-reset`

```json
{
  "phone": "01012345678"
}
```

**Response (OTP included here only for testing):**
```json
{
  "otp": "123456"
}
```

---

### 🔹 Verify OTP & reset password
`POST /auth/verify-reset`

```json
{
  "phone": "01012345678",
  "otp": "123456",
  "new_password": "newPass456"
}
```

---

## 📜 Notes

- OTPs are hashed before being stored in the database.  
- OTPs expire after **5 minutes** (`OTP_TTL_SECONDS = 300`).  
- OTP resend cooldown is **1 second** (`OTP_RESEND_COOLDOWN = 1`).  
- `send_sms_stub` currently prints the OTP to the console — replace it with Twilio, Vonage, or any real SMS provider.

---

## ✅ Future Improvements

- Integrate real SMS sending (Twilio, Humo, etc.)  
- Add account activation with OTP at registration  
- Implement refresh tokens + logout  
- Add 2FA (Google Authenticator, etc.)  
# FastAPI-MicroAPP
