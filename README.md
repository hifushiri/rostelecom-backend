# Rostelecom Project Management API

A FastAPI-based backend for managing projects with a web interface and analytics, as per Rostelecom's case requirements.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Install Prisma CLI: `npm install -g prisma`
3. Set up PostgreSQL and set `DATABASE_URL` environment variable (e.g., `export DATABASE_URL=postgresql://user:pass@localhost:5432/db`)
4. Generate Prisma client: `prisma generate --schema=app/database/schema.prisma`
5. Apply migrations: `prisma db push --schema=app/database/schema.prisma`
6. Run the app: `uvicorn app.main:app --reload`

## Features
- User authentication with JWT
- Role-based access (Admin, Analyst, User)
- Project CRUD with history tracking
- Dictionary management for dropdowns
- Report generation with export to Excel/PDF
- Dashboard stats
- Supports ALT Linux (Python-based)

## Notes
- 2FA is not implemented (add pyotp for production).
- Frontend integration assumes Blade templates (not included).
- Corporate colors handled by frontend.
- Responsive design handled by frontend.
