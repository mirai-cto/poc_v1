import os
import json
from typing import List, Dict
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
def plan_tool_strategy(valid_tools: List[Dict], features: List[Dict], material: str, machine: Dict) -> List[Dict]:
    """
    Uses OpenAI LLM to select tools based on CAD features, material, and machine.

    Parameters
    ----------
    valid_tools : List[Dict]
        Tools filtered for material compatibility.
    features : List[Dict]
        Parsed CAD features (diameter, feature type, etc).
    material : str
        Selected workpiece material (e.g., 'Aluminum').
    machine : Dict
        Dict of machine constraints (e.g., max_rpm).

    Returns
    -------
    List[Dict]
        List of selected toolpaths, formatted for frontend display.
    """
    prompt = f"""
You are a machining expert AI. Select one best-fit cutting tool for each CAD feature
based on the provided material and machine spindle constraints.

Material: {material}
Machine Info: {json.dumps(machine, indent=2)}
Features: {json.dumps(features, indent=2)}

Available Tools:
{json.dumps(valid_tools[:10], indent=2)}  # Only first 10 tools shown

For each feature, return:
- "feature": the CAD feature
- "selected_tool": either the "tool_id" or "name" from the tool
- "reason": why you selected that tool

Only return valid JSON list of objects. No extra explanation.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        content = response.choices[0].message.content.strip()
        parsed = json.loads(content)
    except Exception as e:
        print("❌ LLM tool planning failed:", e)
        return []

    # Convert LLM response back to full tool info for frontend
    frontend_ready = []

    for item in parsed:
        selected = next(
            (tool for tool in valid_tools if
             tool["tool_id"] == item.get("selected_tool") or
             tool["name"].lower() == str(item.get("selected_tool", "")).lower()),
            None
        )

        if selected:
            frontend_ready.append({
                "feature": item.get("feature", {}),
                "selected_tool": {
                    "name": selected.get("name"),
                    "type": selected.get("type"),
                    "material": selected.get("material"),
                    "diameter": selected.get("diameter"),
                    "flute_count": selected.get("flute_count"),
                    "coating": selected.get("coating"),
                    "center_cutting": selected.get("center_cutting"),
                    "manufacturer": selected.get("manufacturer"),
                    "product_link": selected.get("product_link"),
                    "image_link": selected.get("image_link"),
                },
                "reason": item.get("reason", "")
            })

    return frontend_ready
