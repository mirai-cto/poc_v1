from typing import List, Dict

from app.services.cad_parser import process_cad_file

def plan_tool_strategy(valid_tools: List[Dict], features: List[Dict], material: str, machine: Dict) -> List[Dict]:
    # Placeholder logic
    recommendations = []
    for i, feature in enumerate(features):
        if i < len(valid_tools):
            recommendations.append({
                "feature": feature,
                "tool": valid_tools[i],
                "strategy": "roughing + finishing"
            })
    return recommendations

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
    - This function performs 4 key steps:
        1. Parses the CAD file into geometric features (diameter, position, type).
        2. Retrieves material properties and maps them to generalized material classes.
        3. Retrieves machine spindle limits (e.g., Max RPM) and other constraints.
        4. Matches filtered tools to features using the `plan_tool_strategy` function.
    - The material name is normalized using `ALLOY_TO_CLASS` mapping for filtering.
    - The actual tool-feature matching is handled by a separate planner module.
    """

    print("🧠 Inside recommend_from_cad")

    # 1. Extract CAD features
    features = process_cad_file(cad_bytes)

    # 2. Get material info
    mat = db.query(Material).filter(Material.name.ilike(material)).first()
    material_hardness = mat.hardness if mat else 1.0
 
    # 3. Get machine spindle info
    machine = db.query(Machine).filter(Machine.title.ilike(machine_type)).first()
    spindle_data = {}
    max_rpm = 10000  # fallback default
    if machine and machine.spindle_json:
        spindle_data = json.loads(machine.spindle_json)
        max_rpm_str = spindle_data.get("Max Speed", "")
        if isinstance(max_rpm_str, str) and "rpm" in max_rpm_str:
            max_rpm = int(max_rpm_str.replace("rpm", "").strip())
    
    # 4. Filter valid tools
    all_tools = db.query(Tool).all() # Get all tools from DB
    mat: Material = db.query(Material).filter(Material.name.ilike(material)).first()
    if not mat:
        raise ValueError("Material not found.")
    valid_tools = filter_valid_tools(tools=all_tools, material_class=mat, max_rpm=max_rpm, features=features)

    # 🧾 Debug: Show how many tools passed filtering
    print(f"🔧 Valid tools after filtering: {len(valid_tools)}")
    for tool in valid_tools:
        print(f"✅ {tool['name']} | Ø {tool['diameter']} mm | Max DoC: {tool['max_depth_of_cut']} mm | RPM: {tool['max_rpm']}")  

    # 5. LLM-style planning to match tools to features
    selected_toolpaths = plan_tool_strategy(
        valid_tools=valid_tools,
        features=features,
        material=material,
        machine={"max_rpm": max_rpm, "spindle_data": spindle_data}
    )

    print(f"✅ Tool recommendations generated: {len(selected_toolpaths)}")
    return selected_toolpaths
