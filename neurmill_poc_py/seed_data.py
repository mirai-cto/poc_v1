import pandas as pd
import json
from database import SessionLocal
import models
import ast


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
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        machine = models.Machine(
            title=row.get('title'),
            description=row.get('description'),
            product_link=row.get('product_link'),
            price_json=json.dumps(ast.literal_eval(row.get('price_json', '{}'))),
            travels_json=json.dumps(ast.literal_eval(row.get('travels_json', '{}'))),
            spindle_json=json.dumps(ast.literal_eval(row.get('spindle_json', '{}'))),
            table_json=json.dumps(ast.literal_eval(row.get('table_json', '{}'))),
            feedrates_json=json.dumps(ast.literal_eval(row.get('feedrates_json', '{}'))),
            axis_motors_json=json.dumps(ast.literal_eval(row.get('axis_motors_json', '{}'))),
            tool_changer_json=json.dumps(ast.literal_eval(row.get('tool_changer_json', '{}'))),
            general_json=json.dumps(ast.literal_eval(row.get('general_json', '{}'))),
            air_requirements_json=json.dumps(ast.literal_eval(row.get('air_requirements_json', '{}'))),
            electrical_spec_json=json.dumps(ast.literal_eval(row.get('electrical_spec_json', '{}'))),
            shipping_dims_json=json.dumps(ast.literal_eval(row.get('shipping_dims_json', '{}'))),
            trunnion_json=json.dumps(ast.literal_eval(row['trunnion_json'])) if pd.notna(row.get('trunnion_json')) else None
        )
        db.add(machine)
    db.commit()
    db.close()
    print("✅ Machines loaded successfully.")

def load_materials(csv_path):
    db = SessionLocal()
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        material = models.Material(
            name=row.get('name'),
            category=row.get('category'),
            hardness=row.get('hardness', 0.0),
            machinability=row.get('machinability', 0.0)
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
    load_tools("/Users/nmitra28/Desktop/poc_v1/end_mills_cleaned.csv")
    load_machines("/Users/nmitra28/Desktop/poc_v1/vf-series-ds.csv")