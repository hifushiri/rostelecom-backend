from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.database.prisma import prisma
from app.utils.constants import SECRET_KEY, ALGORITHM
import pyotp

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def authenticate_user(username: str, password: str):
    user = await prisma.user.find_unique(where={"username": username})
    if not user or not pwd_context.verify(password, user.password):
        return None
    return user

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_otp(username: str) -> str:
    # Generate a time-based OTP secret
    totp = pyotp.TOTP(pyotp.random_base32())
    # In production, store secret in user record or cache
    # For simplicity, we'll just return it and print (mock sending via email/SMS)
    return totp.now()

def verify_otp(username: str, otp: str) -> bool:
    # In production, retrieve stored secret
    # For simplicity, generate a new TOTP and verify
    totp = pyotp.TOTP(pyotp.random_base32())
    return totp.verify(otp)