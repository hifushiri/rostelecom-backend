from pydantic import BaseModel
from typing import Optional

class DictionaryTypeCreate(BaseModel):
    name:str

class DictionaryType(BaseModel):
    id: int
    name: str

class DictionaryItemCreate(BaseModel):
    type_id: int
    value: str
    probability: Optional[float] = None

class DictionaryItem(BaseModel):
    id: int
    type_id: int
    value: str
    probability: Optional[float]
