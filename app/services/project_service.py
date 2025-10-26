from fastapi import HTTPException
from app.database.prisma import prisma
from app.models.project import ProjectCreate, ProjectUpdate, Project
from app.models.user import User

async def log_change(project_id: int, user_id: int, field: str, old_value: str, new_value: str):
    await prisma.changehistory.create(
        data={
            "project_id": project_id,
            "user_id": user_id,
            "field": field,
            "old_value": old_value,
            "new_value": new_value,
        }
    )

async def create_project(project: ProjectCreate, current_user: User) -> Project:
    # Validate dictionary items
    service = await prisma.dictionaryitem.find_unique(where={"id": project.service_id})
    type_service = await prisma.dictionarytype.find_unique(where={"name": "service"})
    if not service or service.type_id != type_service.id:
        raise HTTPException(400, "Invalid service")
    # Similar for payment_type, stage, business_segment
    stage = await prisma.dictionaryitem.find_unique(where={"id": project.stage_id})
    if not stage or stage.probability is None:
        raise HTTPException(400, "Invalid stage")
    # Validate conditional fields
    if project.assessment_id and not project.forecast_accepted:
        raise HTTPException(400, "Assessment only if forecast accepted")
    if project.industry_manager and not project.industry_solution:
        raise HTTPException(400, "Industry manager only if industry solution")
    if project.project_number and not project.industry_solution:
        raise HTTPException(400, "Project number only if industry solution")
    
    data = project.dict()
    data["probability"] = stage.probability
    db_project = await prisma.project.create(data=data)
    await log_change(db_project.id, current_user.id, "created", "", str(db_project.id))
    return Project(**db_project.__dict__)

async def update_project(project_id: int, update_data: ProjectUpdate, current_user: User) -> Project:
    project = await prisma.project.find_unique(where={"id": project_id})
    if not project:
        raise HTTPException(404, "Project not found")
    
    data = update_data.dict(exclude_unset=True)
    if "stage_id" in data:
        stage = await prisma.dictionaryitem.find_unique(where={"id": data["stage_id"]})
        if not stage:
            raise HTTPException(400, "Invalid stage")
        data["probability"] = stage.probability
        await log_change(project_id, current_user.id, "stage_id", str(project.stage_id), str(data["stage_id"]))
    
    for field, new_value in data.items():
        if field == "probability": continue
        old_value = getattr(project, field)
        if old_value != new_value:
            await log_change(project_id, current_user.id, field, str(old_value), str(new_value))
    
    updated = await prisma.project.update(where={"id": project_id}, data=data)
    return Project(**updated.__dict__)