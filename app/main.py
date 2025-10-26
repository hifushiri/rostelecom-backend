from fastapi import FastAPI
from app.routers import auth, users, dictionaries, projects, revenues, costs, reports, dashboard
from app.database.prisma import prisma
from app.utils.constants import DICT_TYPES
from app.utils.dictionary_loader import load_dictionaries_from_file

app = FastAPI(title="Rostelecom Project Management API")

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(dictionaries.router)
app.include_router(projects.router)
app.include_router(revenues.router)
app.include_router(costs.router)
app.include_router(reports.router)
app.include_router(dashboard.router)

@app.on_event("startup")
async def startup():
    await prisma.connect()
    # Initialize dictionary types
    for name in DICT_TYPES:
        existing = await prisma.dictionarytype.find_unique(where={"name": name})
        if not existing:
            await prisma.dictionarytype.create(data={"name": name})
    # Load dictionaries from file (assumes dict.json in project root)
    try:
        await load_dictionaries_from_file("dict.json")
    except Exception as e:
        print(f"Warning: Could not load dictionaries: {e}")

@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()