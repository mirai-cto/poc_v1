from typing import Dict, List, Tuple
import random
import json
from models import Tool, Material, Machine

def process_cad_file(file_bytes):
    """
    Simulates parsing a CAD file and extracting features.
    """
    # Just return a hardcoded list of features for now
    return ["pocket", "hole", "slot"]

def recommend_from_cad(cad_bytes: bytes, material: str, machine_type: str, db) -> List[Dict]:
    """
    Recommends tools by delegating CAD feature extraction and combining
    it with material + machine constraints.
    """
    print("Inside recommend_from_cad")

    # Step 1: Extract features from CAD
    features = process_cad_file(cad_bytes)  # returns a list like ["pocket", "slot", "hole"]

    # Step 2: Get material hardness from DB
    mat = db.query(Material).filter(Material.name.ilike(material)).first()
    material_hardness = mat.hardness if mat else 1.0

    # Step 3: Get machine spindle limits
    machine = db.query(Machine).filter(Machine.title.ilike(machine_type)).first()
    max_rpm = 10000
    if machine and machine.spindle_json:
        spindle_data = json.loads(machine.spindle_json)
        max_rpm = spindle_data.get("max_rpm", max_rpm)

    # Step 4: Dummy rule-based mapping
    tool_map = {
        "pocket": {"tool": "12mm Flat Endmill", "base_rpm": 8000},
        "hole": {"tool": "6mm Drill Bit", "base_rpm": 5000},
        "slot": {"tool": "8mm Ball Nose", "base_rpm": 7000}
    }
    default_tool = {"tool": "Generic Tool", "base_rpm": 6000}

    # Step 5: Generate one recommendation per feature
    recommendations = []
    for feature in features:
        base = tool_map.get(feature, default_tool)
        rpm = int(base["base_rpm"] * (1 - 0.05 * material_hardness))
        rpm = min(rpm, max_rpm)

        recommendations.append({
            "tool": base["tool"],
            "tool_type": feature,
            "speed": rpm,
            "feed": 0.002,  # dummy value
            "material": material,
            "operation": feature
        })

    return recommendations

def calculate_speed_feed(tool_name, wear_score):
    """
    Adjusts speed and feed based on tool wear score.
    """
    base_rpm = 8000
    base_feed = 600

    factor = 1 - (wear_score / 2)
    adjusted_rpm = int(base_rpm * factor)
    adjusted_feed = int(base_feed * factor)

    return {
        "tool": tool_name,
        "rpm": adjusted_rpm,
        "feed": adjusted_feed,
        "max_doc": round(1.0 - wear_score * 0.3, 2),
        "chatter_risk": "medium" if wear_score > 0.6 else "low"
    }
