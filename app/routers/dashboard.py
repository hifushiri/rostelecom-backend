from fastapi import APIRouter, Depends
from app.models.user import User
from app.dependencies import get_current_user
from app.services.report_service import get_dashboard_stats
from app.database.prisma import prisma
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/")
async def get_dashboard(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user)
):
    return await get_dashboard_stats(start_date, end_date)

@router.get("/gantt/{project_id}")
async def get_gantt_data(project_id: int, current_user: User = Depends(get_current_user)):
    project = await prisma.project.find_unique(where={"id": project_id})
    if not project:
        raise HTTPException(404, "Project not found")
    
    # Get stage changes from history
    stage_changes = await prisma.changehistory.find_many(
        where={"project_id": project_id, "field": "stage_id"},
        order={"changed_at": "asc"},
        include={"project": {"include": {"stage": True}}}
    )
    
    # Get revenue and cost periods
    revenues = await prisma.revenue.find_many(where={"project_id": project_id})
    costs = await prisma.cost.find_many(where={"project_id": project_id})
    
    gantt_data = {
        "stages": [
            {
                "stage": change.project.stage.value,
                "start": change.changed_at.isoformat(),
                "end": (await prisma.changehistory.find_first(
                    where={"project_id": project_id, "field": "stage_id", "changed_at": {"gt": change.changed_at}},
                    order={"changed_at": "asc"}
                )).changed_at.isoformat() if await prisma.changehistory.find_first(
                    where={"project_id": project_id, "field": "stage_id", "changed_at": {"gt": change.changed_at}}
                ) else datetime.utcnow().isoformat()
            } for change in stage_changes
        ],
        "revenues": [
            {
                "amount": r.amount,
                "date": f"{r.year}-{r.month:02d}-01" if r.year and r.month else None
            } for r in revenues
        ],
        "costs": [
            {
                "amount": c.amount,
                "date": f"{c.year}-{c.month:02d}-01" if c.year and c.month else None
            } for c in costs
        ]
    }
    
    return gantt_data