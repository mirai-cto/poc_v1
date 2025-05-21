import pandas as pd
import json
from database import SessionLocal
from models import Machine
import models
import ast

def safe_eval(field_val, field_name, title):
    try:
        if isinstance(field_val, dict):
            return field_val
        elif isinstance(field_val, str):
            return eval(field_val)
    except Exception as e:
        print(f"❌ Failed to parse {field_name} for {title}: {e}")
    return {}

def load_tools(csv_path):
    db = SessionLocal()
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        # Some fields might be empty; use safe parsing
        tool = models.Tool(
            name=row.get('name'),
            type=row.get('type'),
            diameter=row.get('diameter', 0.0),
            shank_diameter=row.get('shank_diameter', 0.0),
            flute_count=row.get('flute_count', 0),
            material=row.get('material'),
            coating=row.get('coating'),
            max_speed=row.get('max_speed', 0.0),
            max_feed=row.get('max_feed', 0.0),
            cutting_length=row.get('cutting_length', 0.0),
            overall_length=row.get('overall_length', 0.0),
            helix_angle=row.get('helix_angle', 0.0),
            workpiece_materials=json.dumps(ast.literal_eval(row.get('workpiece_materials', '[]'))),
            center_cutting=row.get('center_cutting'),
            price_usd=row.get('price_usd', 0.0),
            manufacturer=row.get('manufacturer'),
            max_depth_of_cut=row.get('max_depth_of_cut', 0.0),
            max_rpm=row.get('max_rpm', 0.0),
            speed_feed_link=row.get('speed_feed_link'),
            product_link=row.get('product_link'),
            image_link=row.get('image_link')
        )
        db.add(tool)
    db.commit()
    db.close()
    print("✅ Tools loaded successfully.")

def load_machines(csv_path):
    db = SessionLocal()
    
    # 💥 Step 1: Clear old records
    db.query(Machine).delete()
    
    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        title = row.get('title', 'Unknown')
        machine = Machine(
            title=title,
            description=row.get('description'),
            product_link=row.get('product_link'),

            price_json=json.dumps(safe_eval(row.get('price'), 'price', title)),
            travels_json=json.dumps(safe_eval(row.get('Travels'), 'Travels', title)),
            spindle_json=json.dumps(safe_eval(row.get('Spindle'), 'Spindle', title)),
            table_json=json.dumps(safe_eval(row.get('Table'), 'Table', title)),
            feedrates_json=json.dumps(safe_eval(row.get('Feedrates'), 'Feedrates', title)),
            axis_motors_json=json.dumps(safe_eval(row.get('Axis Motors'), 'Axis Motors', title)),
            tool_changer_json=json.dumps(safe_eval(row.get('Tool Changer'), 'Tool Changer', title)),
            general_json=json.dumps(safe_eval(row.get('General'), 'General', title)),
            air_requirements_json=json.dumps(safe_eval(row.get('Air Requirements'), 'Air Requirements', title)),
            electrical_spec_json=json.dumps(safe_eval(row.get('Electrical Specification'), 'Electrical Specification', title)),
            shipping_dims_json=json.dumps(safe_eval(row.get('Dimensions - Shipping'), 'Dimensions - Shipping', title)),
            trunnion_json=json.dumps(safe_eval(row.get('Trunnion'), 'Trunnion', title)) if pd.notna(row.get('Trunnion')) else None
        )

        db.add(machine)

    db.commit()
    db.close()
    print("✅ Machines loaded successfully.")

def load_materials(csv_path):
    db = SessionLocal()
    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        name = row.get("Material")
        hardness_raw = row.get("Hardness", "")

        # Clean name
        if isinstance(name, str):
            name = name.split("/")[0].strip()

        # Parse hardness
        try:
            if "-" in str(hardness_raw):
                parts = hardness_raw.replace("–", "-").split("-")
                hardness = (float(parts[0].strip()) + float(parts[1].strip())) / 2
            else:
                hardness = float(hardness_raw)
        except:
            hardness = 0.0

        # Skip if already exists
        existing_material = db.query(models.Material).filter_by(name=name).first()
        if existing_material:
            continue

        # Insert new material
        material = models.Material(
            name=name,
            hardness=hardness,
            machinability=50.0  # placeholder
        )
        db.add(material)

    db.commit()
    db.close()
    print("✅ Materials loaded successfully.")


def load_operations(csv_path):
    db = SessionLocal()
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        operation = models.Operation(
            name=row.get('name'),
            description=row.get('description'),
            recommended_speed=row.get('recommended_speed', 0.0),
            recommended_feed=row.get('recommended_feed', 0.0)
        )
        db.add(operation)
    db.commit()
    db.close()
    print("✅ Operations loaded successfully.")

if __name__ == "__main__":
    load_tools("/Users/nkhormaei/Projects/poc_v1/end_mills_cleaned.csv")
    load_machines("/Users/nkhormaei/Projects/poc_v1/vf-series-ds.csv")
    load_materials("/Users/nkhormaei/Projects/poc_v1/all_materials_cleaned.csv")