from app.db.database import SessionLocal
def get_db():
    db = SessionLocal()  # ← pulls from your engine/session config
    try:
        yield db          # ← allows FastAPI to inject this into route handlers
    finally:
        db.close() 