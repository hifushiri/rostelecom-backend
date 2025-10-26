#!/bin/bash

# Project root directory
PROJECT_DIR="project"

# Create project root
mkdir -p "$PROJECT_DIR"

# Create app directory and subdirectories
mkdir -p "$PROJECT_DIR/app"
mkdir -p "$PROJECT_DIR/app/models"
mkdir -p "$PROJECT_DIR/app/routers"
mkdir -p "$PROJECT_DIR/app/services"
mkdir -p "$PROJECT_DIR/app/utils"
mkdir -p "$PROJECT_DIR/app/database"

# Create files in app directory
touch "$PROJECT_DIR/app/__init__.py"
touch "$PROJECT_DIR/app/main.py"
touch "$PROJECT_DIR/app/dependencies.py"

# Create model files
touch "$PROJECT_DIR/app/models/__init__.py"
touch "$PROJECT_DIR/app/models/user.py"
touch "$PROJECT_DIR/app/models/project.py"
touch "$PROJECT_DIR/app/models/dictionary.py"
touch "$PROJECT_DIR/app/models/report.py"

# Create router files
touch "$PROJECT_DIR/app/routers/__init__.py"
touch "$PROJECT_DIR/app/routers/auth.py"
touch "$PROJECT_DIR/app/routers/users.py"
touch "$PROJECT_DIR/app/routers/dictionaries.py"
touch "$PROJECT_DIR/app/routers/projects.py"
touch "$PROJECT_DIR/app/routers/revenues.py"
touch "$PROJECT_DIR/app/routers/costs.py"
touch "$PROJECT_DIR/app/routers/reports.py"
touch "$PROJECT_DIR/app/routers/dashboard.py"

# Create service files
touch "$PROJECT_DIR/app/services/__init__.py"
touch "$PROJECT_DIR/app/services/auth_service.py"
touch "$PROJECT_DIR/app/services/project_service.py"
touch "$PROJECT_DIR/app/services/report_service.py"
touch "$PROJECT_DIR/app/services/export_service.py"

# Create utils files
touch "$PROJECT_DIR/app/utils/__init__.py"
touch "$PROJECT_DIR/app/utils/constants.py"

# Create database files
touch "$PROJECT_DIR/app/database/__init__.py"
touch "$PROJECT_DIR/app/database/prisma.py"
touch "$PROJECT_DIR/app/database/schema.prisma"

# Create root-level files
touch "$PROJECT_DIR/requirements.txt"
touch "$PROJECT_DIR/README.md"

# Populate requirements.txt with dependencies
cat <<EOL > "$PROJECT_DIR/requirements.txt"
fastapi
uvicorn
prisma-client-py
pydantic
passlib[bcrypt]
python-jose[cryptography]
python-multipart
openpyxl
reportlab
EOL

# Populate README.md with basic content
cat <<EOL > "$PROJECT_DIR/README.md"
# Rostelecom Project Management API

A FastAPI-based backend for managing projects with a web interface and analytics, as per Rostelecom's case requirements.

## Setup

1. Install dependencies: \`pip install -r requirements.txt\`
2. Install Prisma CLI: \`npm install -g prisma\`
3. Set up PostgreSQL and set \`DATABASE_URL\` environment variable (e.g., \`export DATABASE_URL=postgresql://user:pass@localhost:5432/db\`)
4. Generate Prisma client: \`prisma generate --schema=app/database/schema.prisma\`
5. Apply migrations: \`prisma db push --schema=app/database/schema.prisma\`
6. Run the app: \`uvicorn app.main:app --reload\`

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
EOL

# Make the script executable
chmod +x "$0"

echo "Project structure initialized successfully in $PROJECT_DIR!"
echo "Next steps:"
echo "1. Populate the files with the provided code."
echo "2. Set up PostgreSQL and configure DATABASE_URL."
echo "3. Install dependencies: pip install -r $PROJECT_DIR/requirements.txt"
echo "4. Install Prisma CLI: npm install -g prisma"
echo "5. Generate Prisma client: prisma generate --schema=$PROJECT_DIR/app/database/schema.prisma"
echo "6. Apply migrations: prisma db push --schema=$PROJECT_DIR/app/database/schema.prisma"
echo "7. Run the app: uvicorn app.main:app --reload"