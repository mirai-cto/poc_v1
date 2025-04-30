from typing import Dict, List, Tuple
import random

class ToolRecommender:
    def __init__(self):
        self.tools = {
            "end_mill": ["4-flute carbide", "2-flute carbide", "3-flute carbide"],
            "face_mill": ["4-insert carbide", "6-insert carbide"],
            "drill": ["HSS", "Carbide"],
        }
        
        self.materials = {
            "aluminum": {"speed_factor": 1.0, "feed_factor": 1.0},
            "steel": {"speed_factor": 0.5, "feed_factor": 0.5},
            "stainless": {"speed_factor": 0.3, "feed_factor": 0.3},
        }
        
        self.operations = {
            "roughing": {"speed_factor": 1.0, "feed_factor": 1.0},
            "finishing": {"speed_factor": 1.2, "feed_factor": 0.8},
        }

    def recommend_tool(self, material: str, operation: str, feature_type: str) -> Dict:
        # Simple rule-based recommendation
        if feature_type == "pocket":
            tool_type = "end_mill"
        elif feature_type == "face":
            tool_type = "face_mill"
        elif feature_type == "hole":
            tool_type = "drill"
        else:
            tool_type = "end_mill"  # default

        tool = random.choice(self.tools[tool_type])
        
        # Calculate speed and feed
        base_speed = 1000  # SFM
        base_feed = 0.005  # IPT
        
        material_factors = self.materials.get(material, {"speed_factor": 1.0, "feed_factor": 1.0})
        operation_factors = self.operations.get(operation, {"speed_factor": 1.0, "feed_factor": 1.0})
        
        speed = base_speed * material_factors["speed_factor"] * operation_factors["speed_factor"]
        feed = base_feed * material_factors["feed_factor"] * operation_factors["feed_factor"]
        
        return {
            "tool": tool,
            "speed": round(speed, 2),
            "feed": round(feed, 4),
            "tool_type": tool_type,
            "material": material,
            "operation": operation
        }

    def calculate_speed_feed(self, tool: str, material: str, operation: str) -> Tuple[float, float]:
        recommendation = self.recommend_tool(material, operation, "general")
        return recommendation["speed"], recommendation["feed"] 
    

    