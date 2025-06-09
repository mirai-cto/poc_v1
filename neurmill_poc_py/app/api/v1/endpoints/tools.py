# app/api/v1/endpoints/tool.py

from http.client import HTTPException
from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.db import crud
from app.db.models import Tool
from sqlalchemy.orm import Session
from app.api.v1.dependencies import get_db
from app.services.tool_selector import ToolRecommender

router = APIRouter()

@router.post("/tools/recommend")
async def recommend_tools(
    cad_file: UploadFile = File(...),
    material: str = Form(...),         # Required form field
    machine_type: str = Form(...),     # Required form field
    db: Session = Depends(get_db)
):
    cad_bytes = await cad_file.read()
    recommender = ToolRecommender(db=db)
    result = recommender.recommend_tools(
        cad_bytes=cad_bytes,
        material=material,
        machine_type=machine_type
    )
    return {"recommendations": result}

@router.get("/tools/{tool_id}")
def get_tool_by_id(tool_id: int, db: Session = Depends(get_db)):
    tool = crud.get_tool(db, tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool

@router.get("/tools")
def get_all_tools(db: Session = Depends(get_db)):
    return db.query(Tool).all()

router.get("/tools/{material}")
def get_tools_by_material(material: str, db: Session = Depends(get_db)):
    return crud.get_tools_by_material(db, material)

@router.post("/tools")
def create_tool(tool_data: dict, db: Session = Depends(get_db)):
    return crud.create_tool(db, tool_data)
