from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.revenue import RevenueCreate, RevenueUpdate, Revenue
from app.models.user import User
from app.dependencies import get_current_user
from app.database.prisma import prisma
from app.services.project_service import log_change

router = APIRouter(prefix="/projects/{project_id}/revenues", tags=["revenues"])

@router.post("/", response_model=Revenue)
async def create_revenue(project_id: int, revenue: RevenueCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in ["ADMIN", "ANALYST", "USER"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    project = await prisma.project.find_unique(where={"id": project_id})
    if not project:
        raise HTTPException(404, "Project not found")
    status = await prisma.dictionaryitem.find_unique(where={"id": revenue.status_id})
    if not status or status.type_id != (await prisma.dictionarytype.find_unique(where={"name": "revenue_status"})).id:
        raise HTTPException(400, "Invalid revenue status")
    data = revenue.dict()
    data["project_id"] = project_id
    db_revenue = await prisma.revenue.create(data=data)
    await log_change(project_id, current_user.id, "revenue_added", "", str(db_revenue.id))
    return Revenue(**db_revenue.__dict__)

@router.get("/", response_model=List[Revenue])
async def get_revenues(project_id: int, current_user: User = Depends(get_current_user)):
    project = await prisma.project.find_unique(where={"id": project_id})
    if not project:
        raise HTTPException(404, "Project not found")
    revenues = await prisma.revenue.find_many(where={"project_id": project_id})
    return [Revenue(**r.__dict__) for r in revenues]

@router.get("/{revenue_id}", response_model=Revenue)
async def get_revenue(project_id: int, revenue_id: int, current_user: User = Depends(get_current_user)):
    revenue = await prisma.revenue.find_unique(where={"id": revenue_id})
    if not revenue or revenue.project_id != project_id:
        raise HTTPException(404, "Revenue not found")
    return Revenue(**revenue.__dict__)

@router.put("/{revenue_id}", response_model=Revenue)
async def update_revenue(project_id: int, revenue_id: int, update_data: RevenueUpdate, current_user: User = Depends(get_current_user)):
    if current_user.role not in ["ADMIN", "ANALYST", "USER"]:
        raise HTTPException(403, "Not authorized")
    revenue = await prisma.revenue.find_unique(where={"id": revenue_id})
    if not revenue or revenue.project_id != project_id:
        raise HTTPException(404, "Revenue not found")
    data = update_data.dict(exclude_unset=True)
    if "status_id" in data:
        status = await prisma.dictionaryitem.find_unique(where={"id": data["status_id"]})
        if not status or status.type_id != (await prisma.dictionarytype.find_unique(where={"name": "revenue_status"})).id:
            raise HTTPException(400, "Invalid revenue status")
    for field, new_value in data.items():
        old_value = getattr(revenue, field)
        if old_value != new_value:
            await log_change(project_id, current_user.id, f"revenue_{field}", str(old_value), str(new_value))
    updated = await prisma.revenue.update(where={"id": revenue_id}, data=data)
    return Revenue(**updated.__dict__)

@router.delete("/{revenue_id}")
async def delete_revenue(project_id: int, revenue_id: int, current_user: User = Depends(get_current_user)):
    if current_user.role not in ["ADMIN"]:
        raise HTTPException(403, "Not authorized")
    revenue = await prisma.revenue.find_unique(where={"id": revenue_id})
    if not revenue or revenue.project_id != project_id:
        raise HTTPException(404, "Revenue not found")
    await prisma.revenue.delete(where={"id": revenue_id})
    await log_change(project_id, current_user.id, "revenue_deleted", str(revenue_id), "")
    return {"message": "Revenue deleted"}