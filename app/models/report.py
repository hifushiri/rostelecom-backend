from pydantic import BaseModel
from typing import List, Dict

class ReportQuery(BaseModel):
    fields: List[str]
    filters: Dict