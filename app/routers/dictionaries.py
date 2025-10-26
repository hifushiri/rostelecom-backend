from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.dictionary import DictionaryTypeCreate, DictionaryType, DictionaryItemCreate, DictionaryItem
from app.database.prisma import prisma
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/dictionaries", tags=["dictionaries"])

@router.post("/types", response_model=DictionaryType)
async def create_dictionary_type(type: DictionaryTypeCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in ["ADMIN"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return await prisma.dictionarytype.create(data=type.dict())

@router.get("/types", response_model=List[DictionaryType])
async def get_dictionary_types(current_user: User = Depends(get_current_user)):
    return await prisma.dictionarytype.find_many()

@router.post("/items", response_model=DictionaryItem)
async def create_dictionary_item(item: DictionaryItemCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in ["ADMIN"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return await prisma.dictionaryitem.create(data=item.dict())

@router.get("/items", response_model=List[DictionaryItem])
async def get_dictionary_items(type_id: int = None, current_user: User = Depends(get_current_user)):
    if type_id:
        return await prisma.dictionaryitem.find_many(where={"type_id": type_id})
    return await prisma.dictionaryitem.find_many()