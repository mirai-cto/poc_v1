# app/api/v1/endpoints/cad.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.cad_parser import process_cad_file

router = APIRouter()

@router.post("/preview-features")
async def preview_features(file: UploadFile = File(...)):
    cad_bytes = await file.read()
    features = process_cad_file(cad_bytes)
    return {"features": features}

@router.post("/upload")
async def upload_cad(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        raw_features = process_cad_file(file_bytes)
        normalized = [{
            "type": f.get("feature", "unknown"),
            "diameter": f.get("diameter"),
            "depth": f.get("depth"),
            "position": f.get("position")
        } for f in raw_features]
        return {"features": normalized}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to process CAD file")
