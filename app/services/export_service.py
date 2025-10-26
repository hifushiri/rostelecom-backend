from fastapi.responses import Response
from io import BytesIO
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from typing import List, Dict

def export_to_excel(report_data: List[Dict]) -> Response:
    wb = Workbook()
    ws = wb.active
    headers = list(report_data[0].keys()) if report_data else []
    ws.append(headers)
    for row in report_data:
        ws.append([row[h] for h in headers])
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return Response(
        content=buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=report.xlsx"}
    )

def export_to_pdf(report_data: List[Dict]) -> Response:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    y = 750
    for row in report_data:
        c.drawString(100, y, str(row))
        y -= 20
    c.save()
    buffer.seek(0)
    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=report.pdf"}
    )