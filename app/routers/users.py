from fastapi import APIRouter, Depends, HTTPException
from app.models.user import UserCreate, User
from app.dependencies import get_current_user
from app.database.prisma import prisma
from app.services.auth_service import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User)
async def create_user(user: UserCreate, current_user: User = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized")
    hashed_password = get_password_hash(user.password)
    db_user = await prisma.user.create(
        data={
            "username": user.username,
            "password": hashed_password,
            "role": user.role.upper(),
        }
    )
    return User(**db_user.__dict__)