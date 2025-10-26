from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.cost import CostCreate, CostUpdate, Cost
from app.models.user import User
from app.dependencies import get_current_user
from app.database.prisma import prisma
from app.services.project_service import log_change

router = APIRouter(prefix="/projects/{project_id}/costs", tags=["costs"])

@router.post("/", response_model=Cost)
async def create_cost(project_id: int, cost: CostCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in ["ADMIN", "ANALYST", "USER"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    project = await prisma.project.find_unique(where={"id": project_id})
    if not project:
        raise HTTPException(404, "Project not found")
    cost_type = await prisma.dictionaryitem.find_unique(where={"id": cost.cost_type_id})
    status = await prisma.dictionaryitem.find_unique(where={"id": cost.status_id})
    type_cost = await prisma.dictionarytype.find_unique(where={"name": "cost_type"})
    type_status = await prisma.dictionarytype.find_unique(where={"name": "cost_status"})
    if not cost_type or cost_type.type_id != type_cost.id:
        raise HTTPException(400, "Invalid cost type")
    if not status or status.type_id != type_status.id:
        raise HTTPException(400, "Invalid cost status")
    data = cost.dict()
    data["project_id"] = project_id
    db_cost = await prisma.cost.create(data=data)
    await log_change(project_id, current_user.id, "cost_added", "", str(db_cost.id))
    return Cost(**db_cost.__dict__)

@router.get("/", response_model=List[Cost])
async def get_costs(project_id: int, current_user: User = Depends(get_current_user)):
    project = await prisma.project.find_unique(where={"id": project_id})
    if not project:
        raise HTTPException(404, "Project not found")
    costs = await prisma.cost.find_many(where={"project_id": project_id})
    return [Cost(**c.__dict__) for c in costs]

@router.get("/{cost_id}", response_model=Cost)
async def get_cost(project_id: int, cost_id: int, current_user: User = Depends(get_current_user)):
    cost = await prisma.cost.find_unique(where={"id": cost_id})
    if not cost or cost.project_id != project_id:
        raise HTTPException(404, "Cost not found")
    return Cost(**cost.__dict__)

@router.put("/{cost_id}", response_model=Cost)
async def update_cost(project_id: int, cost_id: int, update_data: CostUpdate, current_user: User = Depends(get_current_user)):
    if current_user.role not in ["ADMIN", "ANALYST", "USER"]:
        raise HTTPException(403, "Not authorized")
    cost = await prisma.cost.find_unique(where={"id": cost_id})
    if not cost or cost.project_id != project_id:
        raise HTTPException(404, "Cost not found")
    data = update_data.dict(exclude_unset=True)
    if "cost_type_id" in data:
        cost_type = await prisma.dictionaryitem.find_unique(where={"id": data["cost_type_id"]})
        if not cost_type or cost_type.type_id != (await prisma.dictionarytype.find_unique(where={"name": "cost_type"})).id:
            raise HTTPException(400, "Invalid cost type")
    if "status_id" in data:
        status = await prisma.dictionaryitem.find_unique(where={"id": data["status_id"]})
        if not status or status.type_id != (await prisma.dictionarytype.find_unique(where={"name": "cost_status"})).id:
            raise HTTPException(400, "Invalid cost status")
    for field, new_value in data.items():
        old_value = getattr(cost, field)
        if old_value != new_value:
            await log_change(project_id, current_user.id, f"cost_{field}", str(old_value), str(new_value))
    updated = await prisma.cost.update(where={"id": cost_id}, data=data)
    return Cost(**updated.__dict__)

@router.delete("/{cost_id}")
async def delete_cost(project_id: int, cost_id: int, current_user: User = Depends(get_current_user)):
    if current_user.role not in ["ADMIN"]:
        raise HTTPException(403, "Not authorized")
    cost = await prisma.cost.find_unique(where={"id": cost_id})
    if not cost or cost.project_id != project_id:
        raise HTTPException(404, "Cost not found")
    await prisma.cost.delete(where={"id": cost_id})
    await log_change(project_id, current_user.id, "cost_deleted", str(cost_id), "")
    return {"message": "Cost deleted"}