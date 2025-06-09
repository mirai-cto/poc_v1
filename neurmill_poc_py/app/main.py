from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.endpoints import tools, health, cad, materials, operations, machines

app = FastAPI(
    title="Neuramill POC",
    description="CNC Tool Recommender System API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Include all API routes
app.include_router(tools.router, prefix="/api/v1", tags=["Tools"])
app.include_router(cad.router, prefix="/api/v1", tags=["CAD"])
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(materials.router, prefix="/api/v1", tags=["Materials"])
app.include_router(machines.router, prefix="/api/v1", tags=["Machines"])
