from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # 'ADMIN', 'ANALYST', 'USER'

class User(BaseModel):
    id: int
    username: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str