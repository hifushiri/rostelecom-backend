from fastapi import APIRouter, Depends, HTTPException
from app.models.report import ReportQuery
from app.models.user import User
from app.dependencies import get_current_user
from app.services.report_service import generate_report
from app.services.export_service import export_to_excel, export_to_pdf

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("/", response_model=list)
async def generate_report_endpoint(query: ReportQuery, current_user: User = Depends(get_current_user)):
    if current_user.role not in ["ADMIN", "ANALYST"]:
        raise HTTPException(403, "Not authorized")
    return await generate_report(query)

@router.post("/export/excel")
async def export_report_excel(query: ReportQuery, current_user: User = Depends(get_current_user)):
    if current_user.role not in ["ADMIN", "ANALYST"]:
        raise HTTPException(403, "Not authorized")
    report_data = await generate_report(query)
    return export_to_excel(report_data)

@router.post("/export/pdf")
async def export_report_pdf(query: ReportQuery, current_user: User = Depends(get_current_user)):
    if current_user.role not in ["ADMIN", "ANALYST"]:
        raise HTTPException(403, "Not authorized")
    report_data = await generate_report(query)
    return export_to_pdf(report_data)