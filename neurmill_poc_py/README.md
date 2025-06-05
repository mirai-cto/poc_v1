# NeuralMill POC - CNC Tool Recommender System

This is a full-stack application that helps CNC machinists select appropriate tools and calculate optimal cutting parameters based on material, machine capabilities, and feature types.

## Project Structure

```
neurmill_poc_py/
├── main.py               # FastAPI backend API server
├── models.py             # SQLAlchemy ORM definitions
├── database.py           # SQLite DB config
├── seed_data.py          # Seeds tool & machine data
├── llm_tool_planner.py   # GPT-4-based tool selection logic
├── dummy_ai.py           # Rule-based fallback recommender
├── frontend/
│   └── index.html        # SPA for feature preview + output
└── requirements.txt      # Python dependencies
```

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs with Python
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **Uvicorn**: ASGI server for running FastAPI applications
- **Pydantic**: Data validation and settings management

### Frontend
- **HTML/CSS/JavaScript**: Standard web technologies
- **Bootstrap**: CSS framework for responsive design
- **Fetch API**: For making HTTP requests to the backend

## 🧪 Setup & Usage

### 1. Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Seed the Database

```bash
python seed_data.py
```

This creates `neuralmill.db` from `tools.csv` and `machines.csv`.

### 3. Set OpenAI API Key

```bash
export OPENAI_API_KEY=sk-your-key-here  # Or use a .env file
```

### 4. Run the Server

```bash
python main.py
```

### 5. Open the Frontend

- Open `frontend/index.html` in your browser.
- Or access through the server at `http://localhost:8000`

## Application Flow

### Step 1 – User Interaction

- User selects Material and Machine
- Uploads CAD file (only triggers the flow)
- System shows mocked CAD features for approval
- User clicks **Approve & Get Tools**
- Recommendations are shown with reasoning

### Step 2 – Backend API

| Endpoint                | Description                        |
|------------------------|------------------------------------|
| `/materials`           | Returns materials from DB          |
| `/machines`            | Returns machines from DB           |
| `/api/recommend-tool`  | Triggers LLM-based recommendation  |

### Step 3 – Tool Planning Logic (`llm_tool_planner.py`)

- Takes top 10 tools, features, material, and machine specs
- Calls GPT-4 to select tools for each feature
- Returns structured JSON for the frontend

---

## Features

- Material & machine selection
- Hardcoded CAD feature preview (simulated)
- GPT-4 selects tools with reasoning
- Frontend displays formatted results
- Handles missing data gracefully

---

## Future Plans

- Real CAD parsing (STEP/STL)
- Speed & feed calculations
- Project save/history feature
- User login system
- Integration with CAM software

---

## References

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [OpenAI Python API](https://platform.openai.com/docs/)
- [MDN Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)