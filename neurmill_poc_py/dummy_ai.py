from typing import Dict, List, Tuple
import random

def process_cad_file(file_bytes):
    """
    Simulates parsing a CAD file and extracting features.
    """
    # Just return a hardcoded list of features for now
    return ["pocket", "hole", "slot"]

def recommend_tool(feature, material_hardness, machine_max_rpm):
    """
    Recommend a tool based on feature type, material hardness, and machine limits.
    """
    tool_map = {
        "pocket": {"tool": "12mm Flat Endmill", "base_rpm": 8000},
        "hole": {"tool": "6mm Drill Bit", "base_rpm": 5000},
        "slot": {"tool": "8mm Ball Nose", "base_rpm": 7000}
    }

    default_tool = {"tool": "Generic Tool", "base_rpm": 6000}
    base = tool_map.get(feature, default_tool)

    rpm = int(base["base_rpm"] * (1 - material_hardness * 0.05))
    rpm = min(rpm, machine_max_rpm)

    return {
        "feature": feature,
        "tool": base["tool"],
        "suggested_rpm": rpm
    }

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
