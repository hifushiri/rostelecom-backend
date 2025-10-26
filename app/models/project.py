from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    org_name: str
    org_inn: str
    project_name: str
    service_id: int
    payment_type_id: int
    stage_id: int
    manager: str
    business_segment_id: int
    realization_year: Optional[datetime] = None
    industry_solution: bool = False
    forecast_accepted: bool = False
    via_dzo: bool = False
    needs_leadership_control: bool = False
    assessment_id: Optional[int] = None
    industry_manager: Optional[str] = None
    project_number: Optional[str] = None
    status: Optional[str] = None
    done_in_period: Optional[str] = None
    plans_next_period: Optional[str] = None

class ProjectUpdate(BaseModel):
    org_name: Optional[str] = None
    org_inn: Optional[str] = None
    project_name: Optional[str] = None
    service_id: Optional[int] = None
    payment_type_id: Optional[int] = None
    stage_id: Optional[int] = None
    manager: Optional[str] = None
    business_segment_id: Optional[int] = None
    realization_year: Optional[datetime] = None
    industry_solution: Optional[bool] = None
    forecast_accepted: Optional[bool] = None
    via_dzo: Optional[bool] = None
    needs_leadership_control: Optional[bool] = None
    assessment_id: Optional[int] = None
    industry_manager: Optional[str] = None
    project_number: Optional[str] = None
    status: Optional[str] = None
    done_in_period: Optional[str] = None
    plans_next_period: Optional[str] = None

class Project(BaseModel):
    id: int
    org_name: str
    org_inn: str
    project_name: str
    service_id: int
    payment_type_id: int
    stage_id: int
    probability: float
    manager: str
    business_segment_id: int
    realization_year: Optional[datetime]
    industry_solution: bool
    forecast_accepted: bool
    via_dzo: bool
    needs_leadership_control: bool
    assessment_id: Optional[int]
    industry_manager: Optional[str]
    project_number: Optional[str]
    created_at: datetime
    updated_at: datetime
    status: Optional[str]
    done_in_period: Optional[str]
    plans_next_period: Optional[str]