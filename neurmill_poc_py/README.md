# NeuralMill POC - CNC Tool Recommender System

This is a full-stack application that helps CNC machinists select appropriate tools and calculate optimal cutting parameters based on material, machine capabilities, and feature types.

## Project Structure

```
neurmill_poc_py/
├── main.py            # FastAPI backend server and API endpoints
├── models.py          # SQLAlchemy database models
├── database.py        # Database connection configuration
├── dummy_ai.py        # Tool recommendation and speed/feed calculation logic
├── frontend/          # Frontend files
│   └── index.html     # Single-page application with embedded CSS/JS
└── requirements.txt   # Python dependencies
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

## Seed DB
Seeding the Database

First, load your tools.csv and machines.csv into the database:
```bash
   python seed_data.py
```
It will create a file neuralmill.db in your project directory with your seeded tools and machines.

## Setup Instructions

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
python main.py
```

4. Open the frontend:
- Open `frontend/index.html` directly in your browser
- Or access through the server at `http://localhost:8000`

## Application Flow

1. **User Interface** (`frontend/index.html`):
   - Provides a form for selecting material, operation type, and feature type
   - Displays tool recommendations and cutting parameters
   - Handles user interactions and API calls

2. **Backend API** (`main.py`):
   - `/machines`: Get list of available CNC machines
   - `/materials`: Get list of supported materials
   - `/tools`: Get list of available cutting tools
   - `/upload_cad`: Process CAD files to extract features
   - `/recommend_tools`: Get tool recommendations based on parameters
   - `/calculate_speeds_feeds`: Calculate optimal cutting parameters

3. **Database Layer** (`models.py`, `database.py`):
   - Defines data models for machines, materials, and tools
   - Handles database connections and sessions
   - Provides CRUD operations for data management

4. **Business Logic** (`dummy_ai.py`):
   - Implements tool recommendation algorithms
   - Calculates speed and feed rates
   - Processes CAD files to extract machining features

## Key Features

1. **Tool Recommendation**:
   - Recommends appropriate cutting tools based on:
     - Material properties
     - Machine capabilities
     - Feature types (pockets, holes, slots)
     - Operation type (roughing, finishing)

2. **Cutting Parameter Calculation**:
   - Calculates optimal:
     - Spindle speed (RPM)
     - Feed rate (IPM)
     - Depth of cut
     - Stepover

3. **CAD File Processing**:
   - Extracts machining features from CAD files
   - Identifies required tool types and sizes
   - Suggests machining strategies

## Development Notes

- The application uses a SQLite database for simplicity
- Frontend is a single-page application for easy deployment
- API endpoints follow RESTful conventions
- Error handling and logging are implemented throughout

## Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.1/getting-started/introduction/)
- [JavaScript Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) 