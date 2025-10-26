from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import authenticate_user, create_access_token, generate_otp, verify_otp
from app.models.user import Token, User
from app.dependencies import get_current_user  # Added import
from app.utils.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Generate OTP for 2FA
    otp_secret = generate_otp(user.username)
    # In production, send OTP via email/SMS (not implemented here)
    print(f"OTP for {user.username}: {otp_secret}")  # For demo, log OTP
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/verify-otp")
async def verify_otp_endpoint(username: str, otp: str, current_user: User = Depends(get_current_user)):
    if current_user.username != username:
        raise HTTPException(status_code=403, detail="Not authorized")
    if not verify_otp(username, otp):
        raise HTTPException(status_code=401, detail="Invalid OTP")
    return {"message": "OTP verified"}