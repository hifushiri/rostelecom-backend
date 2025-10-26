from pydantic import BaseModel
from typing import Optional

class RevenueCreate(BaseModel):
    year: Optional[int]
    month: Optional[int]
    amount: float
    status_id: int

class RevenueUpdate(BaseModel):
    year: Optional[int] = None
    month: Optional[int] = None
    amount: Optional[float] = None
    status_id: Optional[int] = None

class Revenue(BaseModel):
    id: int
    project_id: int
    year: Optional[int]
    month: Optional[int]
    amount: float
    status_id: int