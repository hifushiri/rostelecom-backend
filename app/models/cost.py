from pydantic import BaseModel
from typing import Optional

class CostCreate(BaseModel):
    year: Optional[int]
    month: Optional[int]
    amount: float
    cost_type_id: int
    status_id: int

class CostUpdate(BaseModel):
    year: Optional[int] = None
    month: Optional[int] = None
    amount: Optional[float] = None
    cost_type_id: Optional[int] = None
    status_id: Optional[int] = None

class Cost(BaseModel):
    id: int
    project_id: int
    year: Optional[int]
    month: Optional[int]
    amount: float
    cost_type_id: int
    status_id: int