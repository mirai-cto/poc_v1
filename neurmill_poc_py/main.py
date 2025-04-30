"""
Main FastAPI application file that serves as the entry point for the CNC Tool Recommender system.
This file sets up the backend server, defines API endpoints, and handles the communication between
the frontend and the business logic layer.
"""
from fastapi import FastAPI, Depends, UploadFile, File, Query, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
import json

# Import local modules
from models import Base, Machine, Material, Tool
from database import engine, get_db
from dummy_ai import recommend_tool, calculate_speed_feed, process_cad_file

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="NeuralMill POC",
    description="CNC Tool Recommender System API",
    version="1.0.0"
)

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory for serving frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Root endpoint - serves the frontend
@app.get("/")
async def read_root():
    """
    Root endpoint that serves the main frontend page.
    Returns the index.html file from the frontend directory.
    """
    return FileResponse('frontend/index.html')

# API Endpoints for data retrieval
@app.get("/machines", response_model=List[dict])
async def get_machines(db: Session = Depends(get_db)):
    """
    Returns a list of all available CNC machines from the database.
    Each machine entry includes its capabilities and specifications.
    """
    machines = db.query(Machine).all()
    return [{
        "id": m.id,
        "title": m.title,
        "spindle info":json.loads(m.spindle_json),
        "description": m.description,
        "product_link": m.product_link
    } for m in machines]

@app.get("/materials", response_model=List[dict])
async def get_materials(db: Session = Depends(get_db)):
    """
    Returns a list of all supported materials from the database.
    Each material entry includes its properties relevant to machining.
    """
    materials = db.query(Material).all()
    return [{"id": m.id, "name": m.name, "hardness": m.hardness, "category": m.category} for m in materials]

@app.get("/tools", response_model=List[dict])
async def get_tools(db: Session = Depends(get_db)):
    """
    Returns a list of all available cutting tools from the database.
    Each tool entry includes its specifications and capabilities.
    """
    tools = db.query(Tool).all()
    return [{"id": t.id, "name": t.name, "diameter": t.diameter, "type": t.type} for t in tools]

# API Endpoints for tool recommendation and parameter calculation
@app.post("/recommend_tools")
async def get_tool_recommendations(
    material_id: int,
    operation_type: str,
    feature_type: str,
    machine_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Recommends appropriate cutting tools based on material, operation type, and feature type.
    Optionally considers machine capabilities if machine_id is provided.
    """
    try:
        recommendations = recommend_tools(material_id, operation_type, feature_type, machine_id, db)
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/calculate_speeds_feeds")
async def get_speeds_feeds(
    tool_id: int,
    material_id: int,
    operation_type: str,
    machine_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Calculates optimal cutting parameters (speeds and feeds) based on tool, material,
    and operation type. Optionally considers machine capabilities if machine_id is provided.
    """
    try:
        parameters = calculate_speeds_feeds(tool_id, material_id, operation_type, machine_id, db)
        return {"parameters": parameters}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# CAD file processing endpoint
@app.post("/upload_cad")
async def upload_cad(file: UploadFile = File(...)):
    """
    Handles CAD file uploads, processes them to extract machining features,
    and returns recommendations based on the extracted features.
    """
    try:
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save the uploaded file
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the CAD file
        features = process_cad_file(file_path)
        
        # Clean up the uploaded file
        os.remove(file_path)
        
        return {"features": features}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
