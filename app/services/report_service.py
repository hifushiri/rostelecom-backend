from fastapi import HTTPException
from app.database.prisma import prisma
from app.models.report import ReportQuery
from typing import List, Dict
from datetime import datetime, timedelta

async def generate_report(query: ReportQuery) -> List[Dict]:
    # Validate fields
    valid_fields = [
        "id", "org_name", "org_inn", "project_name", "service_id", "payment_type_id",
        "stage_id", "probability", "manager", "business_segment_id", "realization_year",
        "industry_solution", "forecast_accepted", "via_dzo", "needs_leadership_control",
        "assessment_id", "industry_manager", "project_number", "created_at", "updated_at",
        "status", "done_in_period", "plans_next_period"
    ]
    for field in query.fields:
        if field not in valid_fields and not field.startswith("revenues.") and not field.startswith("costs."):
            raise HTTPException(400, f"Invalid field: {field}")

    # Build include for related data
    include = {}
    if any(f.startswith("revenues.") for f in query.fields):
        include["revenues"] = True
    if any(f.startswith("costs.") for f in query.fields):
        include["costs"] = True

    # Query projects with filters and include
    projects = await prisma.project.find_many(
        where=query.filters,
        include=include
    )

    # Process results to match requested fields
    result = []
    for project in projects:
        row = {}
        for field in query.fields:
            if field in valid_fields:
                row[field] = getattr(project, field)
            elif field.startswith("revenues."):
                subfield = field.split(".")[1]
                row[field] = [getattr(r, subfield) for r in getattr(project, "revenues", [])]
            elif field.startswith("costs."):
                subfield = field.split(".")[1]
                row[field] = [getattr(c, subfield) for c in getattr(project, "costs", [])]
        result.append(row)
    
    return result

async def get_dashboard_stats(start_date: datetime = None, end_date: datetime = None) -> Dict:
    # Default to last 30 days if no dates provided
    if not start_date:
        start_date = datetime.utcnow() - timedelta(days=30)
    if not end_date:
        end_date = datetime.utcnow()

    # Total projects and revenue
    total_projects = await prisma.project.count()
    total_revenue = await prisma.revenue.aggregate(
        where={"created_at": {"gte": start_date, "lte": end_date}},
        _sum={"amount": True}
    )

    # Projects by stage
    stages = await prisma.dictionaryitem.find_many(where={"type_id": (await prisma.dictionarytype.find_unique(where={"name": "stage"})).id})
    stage_counts = []
    for stage in stages:
        count = await prisma.project.count(where={"stage_id": stage.id})
        stage_counts.append({"stage": stage.value, "count": count})

    # Projects by manager, segment, service
    manager_counts = await prisma.project.group_by(
        by=["manager"],
        count=True,
        sum={"probability": True}
    )
    segment_counts = await prisma.project.group_by(
        by=["business_segment_id"],
        count=True,
        sum={"probability": True}
    )
    service_counts = await prisma.project.group_by(
        by=["service_id"],
        count=True,
        sum={"probability": True}
    )

    # Average stage duration (simplified, needs ChangeHistory analysis for precision)
    stage_durations = []
    for stage in stages:
        changes = await prisma.changehistory.find_many(
            where={"field": "stage_id", "new_value": str(stage.id)},
            include={"project": True}
        )
        durations = []
        for change in changes:
            next_change = await prisma.changehistory.find_first(
                where={"project_id": change.project_id, "field": "stage_id", "changed_at": {"gt": change.changed_at}},
                order={"changed_at": "asc"}
            )
            if next_change:
                duration = (next_change.changed_at - change.changed_at).total_seconds() / 86400  # days
                durations.append(duration)
        avg_duration = sum(durations) / len(durations) if durations else 0
        stage_durations.append({"stage": stage.value, "avg_duration_days": avg_duration})

    return {
        "total_projects": total_projects,
        "total_revenue": total_revenue._sum.amount or 0,
        "stage_counts": stage_counts,
        "manager_counts": manager_counts,
        "segment_counts": segment_counts,
        "service_counts": service_counts,
        "stage_durations": stage_durations
    }