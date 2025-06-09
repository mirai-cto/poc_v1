from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.dependencies import get_db
from app.db import crud
from app.db.models import Tool, Material, Operation

router = APIRouter()

@router.get("/materials")
def get_all_materials(db: Session = Depends(get_db)):
    return db.query(Material).all()

@router.get("/materials/{material_id}")
def get_material_by_id(material_id: int, db: Session = Depends(get_db)):
    material = crud.get_material(db, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

@router.post("/materials")
def create_material(material_data: dict, db: Session = Depends(get_db)):
    return crud.create_material(db, material_data)

