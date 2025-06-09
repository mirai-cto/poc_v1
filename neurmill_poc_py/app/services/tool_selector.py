from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.db.models import Tool, Machine, Material
from app.services.cad_parser import process_cad_file
from app.services.llm_planner import plan_tool_strategy
import json

class ToolRecommender:
    def __init__(self, db: Session):
        self.db = db

    def recommend_tools(
        self,
        cad_bytes: bytes,
        material: str,
        machine_type: str,
        machine_id: Optional[int] = None
    ) -> List[Dict]:
        print("🧠 Running ToolRecommender logic...")

        # Step 1: Get features from CAD
        features = process_cad_file(cad_bytes)

        # Step 2: Query material and machine
        mat: Material = self.db.query(Material).filter(Material.name.ilike(material)).first()
        if not mat:
            raise ValueError("Material not found.")
        
        machine = self.db.query(Machine).filter(Machine.title.ilike(machine_type)).first()
        max_rpm = 10000
        spindle_data = {}

        if machine and machine.spindle_json:
            spindle_data = json.loads(machine.spindle_json)
            max_rpm_str = spindle_data.get("Max Speed", "")
            if isinstance(max_rpm_str, str) and "rpm" in max_rpm_str:
                max_rpm = int(max_rpm_str.replace("rpm", "").strip())

        # Step 3: Filter tools
        all_tools = self.db.query(Tool).all()
        valid_tools = self.filter_valid_tools(all_tools, mat.name, mat.hardness, max_rpm, features)

        # Step 4: Plan with LLM
        return plan_tool_strategy(
            valid_tools=valid_tools,
            features=features,
            material=mat.name,
            machine={"max_rpm": max_rpm, "spindle_data": spindle_data}
        )

    @staticmethod
    def classify_operation(tool: Tool) -> str:
        t = tool.type.lower()
        name = tool.name.lower()
        if "drill" in t or "tap" in t:
            return "drilling"
        if tool.flute_count and tool.flute_count <= 3:
            return "roughing"
        if tool.flute_count and tool.flute_count >= 4:
            return "finishing"
        return "general"

    @staticmethod
    def filter_valid_tools(
        tools: List[Tool],
        material_name: str,
        material_hardness: float,
        max_rpm: int,
        features: List[Dict]
    ) -> List[Dict]:
        valid_tools = []

        for tool in tools:
            try:
                supported_materials = json.loads(tool.workpiece_materials)
            except:
                supported_materials = []

            if not any(material_name.lower() in m.lower() for m in supported_materials):
                continue

            if tool.max_rpm and tool.max_rpm < max_rpm:
                continue

            for feat in features:
                if feat.get("diameter") and tool.diameter > feat["diameter"]:
                    continue
                if feat.get("depth") and tool.max_depth_of_cut and tool.max_depth_of_cut < feat["depth"]:
                    continue

                operation_type = ToolRecommender.classify_operation(tool)

                valid_tools.append({
                    **tool.__dict__,
                    "operation_type": operation_type,
                    "material_hardness": material_hardness,
                    "material_name": material_name
                })
                break

        return valid_tools
