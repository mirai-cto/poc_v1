from typing import Dict, List
import json
from models import Tool, Material, Machine
from llm_tool_planner import plan_tool_strategy

# convert db info of material to something searchable for the tools db 
ALLOY_TO_CLASS = {
    # 🟠 Aluminum Alloys
    "Aluminium 2007": "Aluminum",
    "Aluminium 2017A": "Aluminum",
    "Aluminium 5083": "Aluminum",
    "Aluminium 6060": "Aluminum",
    "Aluminium 6061": "Aluminum",
    "Aluminium 6082": "Aluminum",
    "Aluminium 7075": "Aluminum",

    # 🔵 Stainless Steel
    "Stainless Steel 303": "Stainless Steel",
    "Stainless Steel 304": "Stainless Steel",
    "Stainless Steel 304L": "Stainless Steel",
    "Stainless Steel 316L": "Stainless Steel",
    "Stainless Steel 316Ti": "Stainless Steel",

    # ⚫ Generic Carbon and Alloy Steels
    "Steel 1.0038": "Steel",
    "Steel 1.0503": "Steel",
    "Steel 1.0511": "Steel",
    "Steel 1.0570": "Steel",
    "Steel 1.2842": "Steel",
    "Steel 1.7131": "Steel",
    "Steel 1.7218": "Steel",
    "Steel 1.7225": "Steel",

    # 🟣 Titanium Alloys
    "Titan Grade 2": "Titanium",
    "Titan Grade 5": "Titanium",

    # 🟢 Plastics
    "ABS": "Plastic",
    "Acrylic": "Plastic",
    "PC (Polycarbonate)": "Plastic",
    "PEEK": "Plastic",
    "PEEK glass-filled": "Plastic",
    "Polypropylene (PP)": "Plastic",
    "POM / Delrin acetal": "Plastic",
    "PTFE / Teflon": "Plastic",
    "PVDF / Polyvinylidene fluoride": "Plastic",
    "UHMW PE / Ultra-high-molecular-weight polyethene": "Plastic"
}


def process_cad_file(file_bytes) -> List[Dict]:
    """
    Simulates parsing a CAD file and extracting geometric features.
    Each feature includes type, diameter, and XY position.
    """
    print("🔍 Simulating CAD feature extraction...")
    return [
        {"feature": "pocket", "diameter": 12.0, "position": [10.0, 20.0]},
        {"feature": "hole", "diameter": 2.0, "position": [30.5, 45.2]},
        {"feature": "slot", "diameter": 8.0, "position": [60.0, 10.0]},
    ]


def filter_valid_tools(tools: List[Tool], material_class: str, max_rpm: int) -> List[Dict]:
    """
    Filters tools based on material compatibility and machine spindle limits.

    Args:
        tools (List[Tool]): Raw SQLAlchemy Tool objects.
        material_class (str): Normalized class like "aluminum", "steel", etc.
        max_rpm (int): Max RPM allowed by machine.

    Returns:
        List[Dict]: Filtered tools as dictionaries.
    """
    valid_tools = []
    for tool in tools:
        try:
            supported_materials = json.loads(tool.workpiece_materials)
        except:
            supported_materials = []

        if any(material_class in m.lower() for m in supported_materials):
            print(f"🔍 Tool {tool.name} supports: {supported_materials}")

            valid_tools.append({
                "tool_id": tool.tool_id,
                "name": tool.name,
                "type": tool.type,
                "material": tool.material,
                "diameter": tool.diameter,
                "shank_diameter": tool.shank_diameter,
                "cutting_length": tool.cutting_length,
                "overall_length": tool.overall_length,
                "flute_count": tool.flute_count,
                "helix_angle": tool.helix_angle,
                "coating": tool.coating,
                "center_cutting": tool.center_cutting,
                "price_usd": tool.price_usd,
                "manufacturer": tool.manufacturer,
                "max_depth_of_cut": tool.max_depth_of_cut,
                "max_rpm": tool.max_rpm,
                "speed_feed_link": tool.speed_feed_link,
                "product_link": tool.product_link,
                "image_link": tool.image_link,
            })

    return valid_tools


def recommend_from_cad(cad_bytes: bytes, material: str, machine_type: str, db) -> List[Dict]:
    """
    Recommends cutting tools based on CAD geometry, selected material, and machine capabilities.

    This function simulates CAD feature extraction, filters available tools from the database
    based on material compatibility and spindle speed limits, and then delegates final tool 
    selection to a strategy planner (e.g., an LLM or rules-based function).

    Parameters
    ----------
    cad_bytes : bytes
        Raw binary content of the uploaded CAD file.
    material : str
        Name of the selected workpiece material (e.g., "Aluminium 6061").
    machine_type : str
        Title of the selected machine (e.g., "VF-2SS").
    db : Session
        SQLAlchemy database session for querying tools, machines, and materials.

    Returns
    -------
    List[Dict]
        A list of tool recommendations, each containing tool metadata along with the matched feature.

    Notes
    -----
    - This function performs 5 key steps:
        1. Parses the CAD file into geometric features (diameter, position, type).
        2. Retrieves material properties and maps them to generalized material classes.
        3. Retrieves machine spindle limits (e.g., Max RPM) and other constraints.
        4. Filters tools that support the material and do not exceed machine RPM.
        5. Matches filtered tools to features using the `plan_tool_strategy` function.
    - The material name is normalized using `ALLOY_TO_CLASS` mapping for filtering.
    - The actual tool-feature matching is handled by a separate planner module.
    """

    print("🧠 Inside recommend_from_cad")

    # 1. Extract CAD features
    features = process_cad_file(cad_bytes)

    # 2. Get material info
    mat = db.query(Material).filter(Material.name.ilike(material)).first()
    material_hardness = mat.hardness if mat else 1.0
    print(f"🔎 Looking for material: '{material}'")
    print(f"📦 Found material object: {mat}")

    # 3. Get machine spindle info
    machine = db.query(Machine).filter(Machine.title.ilike(machine_type)).first()
    spindle_data = {}
    max_rpm = 10000  # fallback default
    if machine and machine.spindle_json:
        spindle_data = json.loads(machine.spindle_json)
        max_rpm_str = spindle_data.get("Max Speed", "")
        if isinstance(max_rpm_str, str) and "rpm" in max_rpm_str:
            max_rpm = int(max_rpm_str.replace("rpm", "").strip())
    print(f"🛠 Looking for machine type: '{machine_type}'")
    print(f"📦 Found machine object: {machine}")
    print(f"🔧 Extracted spindle JSON: {spindle_data}")
    print(f"⚙️ Max RPM used: {max_rpm}")

    # 4. Filter valid tools
    all_tools = db.query(Tool).all() # Get all tools from DB
    material_class = ALLOY_TO_CLASS.get(material, material).lower() # Map 'Aluminium 2017A' to 'Aluminium'
    valid_tools = filter_valid_tools(all_tools, material_class, max_rpm)

    # 5. LLM-style planning to match tools to features
    selected_toolpaths = plan_tool_strategy(
        valid_tools=valid_tools,
        features=features,
        material=material,
        machine={"max_rpm": max_rpm, "spindle_data": spindle_data}
    )

    print(f"✅ Tool recommendations generated: {len(selected_toolpaths)}")
    return selected_toolpaths


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
