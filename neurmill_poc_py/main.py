"""
Main FastAPI application file that serves as the entry point for the CNC Tool Recommender system.
This file sets up the backend server, defines API endpoints, and handles the communication between
the frontend and the business logic layer.
"""
from fastapi import FastAPI, Depends, UploadFile, File, Query, Body, HTTPException, APIRouter, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import os
import shutil
import json
import logging
from tool_recommender import ToolRecommender
import ast
import models

# Import local modules
from models import Base, Machine, Material, Tool
from database import engine, get_db
from dummy_ai import recommend_from_cad, calculate_speed_feed, process_cad_file

class ToolRequest(BaseModel):
    material: str
    machine_type: str
    machine_id: Optional[int] = None

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

@app.get("/machines", response_model=List[dict])
async def get_machines(db: Session = Depends(get_db)):
    """
    Returns a list of all available CNC machines from the database,
    including parsed spindle specs (max RPM and power).
    """
    machines = db.query(Machine).all()
    results = []
    for m in machines:
        try:
            # Try both json.loads and ast.literal_eval for fallback
            spindle_data = json.loads(m.spindle_json)
            if isinstance(spindle_data, str):
                spindle_data = ast.literal_eval(spindle_data)
        except Exception as e:
            print(f"❌ Failed to parse spindle_json for {m.title}: {e}")
            spindle_data = {}

        print("Parsed spindle_json for", m.title, "→", spindle_data)

        results.append({
            "id": m.id,
            "title": m.title,
            "description": m.description,
            "product_link": m.product_link,
            "max_rpm": spindle_data.get("Max Speed", "").replace(" rpm", ""),
            "max_power": spindle_data.get("Max Rating", "")
        })
    return results


@app.get("/materials", response_model=List[dict])
async def get_materials(db: Session = Depends(get_db)):
    """
    Returns a list of all supported materials from the database.
    Each material entry includes its properties relevant to machining.
    """
    materials = db.query(Material).all()
    result = [
        {
            "name": m.name,
            "hardness": m.hardness,
            "yield_strength": m.yield_strength
        }
        for m in materials
    ]
    print("✔ Materials fetched:", result) # print statement for debugging
    return result

@app.get("/tools", response_model=List[dict])
async def get_tools(db: Session = Depends(get_db)):
    """
    Returns a list of all available cutting tools from the database.
    Each tool entry includes its specifications and capabilities.
    """
    tools = db.query(Tool).all() # Query all rows from the tools table
    return [{"id": t.id, "name": t.name, "diameter": t.diameter, "type": t.type} for t in tools]

@app.post("/api/recommend-tool")
async def get_tool_recommendations(
    material: str = Form(...),
    machine_type: str = Form(...),
    cad_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Recommends appropriate cutting tools based on uploaded CAD file,
    selected material, and machine type.
    """
    try:
        cad_bytes = await cad_file.read()
        print("📩 Received CAD file for tool recommendation")

        # Use the core recommender class
        tr = ToolRecommender(db)
        
        recommendations = tr.recommend_tools(
            cad_bytes=cad_bytes,
            material=material,
            machine_type=machine_type
        )

        print("✅ Tool recommendations generated")
        return {"recommendations": recommendations}

    except Exception as e:
        print(f"❌ Recommendation error: {e}")
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
        raise HTTPEx
    


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
