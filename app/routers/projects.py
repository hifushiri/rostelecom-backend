from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.project import ProjectCreate, ProjectUpdate, Project
from app.dependencies import get_current_user
from app.services.project_service import create_project, update_project
from app.database.prisma import prisma
from app.models.user import User

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=Project)
async def create_project_endpoint(project: ProjectCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in ["ADMIN", "ANALYST", "USER"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return await create_project(project, current_user)

@router.get("/", response_model=List[Project])
async def get_projects(current_user: User = Depends(get_current_user)):
    projects = await prisma.project.find_many()
    return [Project(**p.__dict__) for p in projects]

@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: int, current_user: User = Depends(get_current_user)):
    project = await prisma.project.find_unique(where={"id": project_id})
    if not project:
        raise HTTPException(404, "Project not found")
    return Project(**project.__dict__)

@router.put("/{project_id}", response_model=Project)
async def update_project_endpoint(project_id: int, update_data: ProjectUpdate, current_user: User = Depends(get_current_user)):
    if current_user.role not in ["ADMIN", "ANALYST", "USER"]:
        raise HTTPException(403, "Not authorized")
    return await update_project(project_id, update_data, current_user)

@router.delete("/{project_id}")
async def delete_project(project_id: int, current_user: User = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(403, "Not authorized")
    project = await prisma.project.find_unique(where={"id": project_id})
    if not project:
        raise HTTPException(404, "Project not found")
    await prisma.project.delete(where={"id": project_id})
    return {"message": "Deleted"}

@router.get("/{project_id}/changes")
async def get_changes(project_id: int, current_user: User = Depends(get_current_user)):
    changes = await prisma.changehistory.find_many(
        where={"project_id": project_id},
        order={"changed_at": "desc"},
        take=10
    )
    return changes