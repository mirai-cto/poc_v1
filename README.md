# CNC Tool Recommender and Speed & Feed Recommendation System

A full-stack application that recommends CNC tools and optimal speed/feed parameters based on CAD files, machine specifications, and tool wear data.

## Project Purpose

This system analyzes CAD models, extracts geometric features, and recommends optimal cutting tools and machining parameters. It considers machine limitations, tool wear, and geometric constraints to provide optimized recommendations for:
- Tool selection for roughing, finishing, and drilling operations
- Speed and feed parameters adjusted for tool wear
- Closed-loop feedback system that improves recommendations over time

## Tech Stack

- **Backend**: Java (Spring Boot)
- **Frontend**: JavaScript (Vite + React)
- **Database**: PostgreSQL
- **ML Module**: Python (standalone service)
- **API Communication**: REST APIs
- **Frontend Package Manager**: npm
- **Data Ingestion**: CSV (machine and tool data)
- **LLM Integration**: OpenAI API

## End-to-End Flow

1. User uploads a STEP (.stp) CAD file via frontend
2. Python parser extracts geometric features (mocked)
3. Features classified by type (hole, slot, chamfer, etc.)
4. Backend filters tools based on machine constraints
5. OpenAI API generates tool recommendations (mocked)
6. User inputs tool wear scores (1-10)
7. System calculates optimized speed/feed parameters
8. User provides performance feedback after job completion
9. System updates tool wear database for future recommendations

```
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
│            │     │            │     │            │     │            │
│   Upload   │────▶│   Parser   │────▶│ Classifier │────▶│ Constraint │
│   CAD      │     │  (Python)  │     │  (Python)  │     │   Filter   │
│            │     │            │     │            │     │            │
└────────────┘     └────────────┘     └────────────┘     └────────────┘
                                                                │
                                                                ▼
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
│            │     │            │     │            │     │            │
│  Feedback  │◀────│ Speed/Feed │◀────│  Tool Wear │◀────│    LLM     │
│   Loop     │     │ Calculator │     │   Input    │     │ Recommender│
│            │     │            │     │            │     │            │
└────────────┘     └────────────┘     └────────────┘     └────────────┘
```

## Setup

### Docker Setup (Recommended)

1. Clone the repository
2. Copy `.env.example` to `.env` and add your OpenAI API key
3. Run `docker-compose up`
4. Access frontend at http://localhost:3000
5. Backend API available at http://localhost:8080

### Local Development Setup

#### Prerequisites:
- Java 17+
- Node.js 16+
- Python 3.8+
- PostgreSQL 14+

#### Steps:
1. Clone the repository
2. Copy `.env.example` to `.env` and add your OpenAI API key
3. Set up PostgreSQL database:
   ```
   cd database
   python seed.py
   ```
4. Start backend:
   ```
   cd backend
   ./mvnw spring-boot:run
   ```
5. Start frontend:
   ```
   cd frontend
   npm install
   npm run dev
   ```
6. Access frontend at http://localhost:3000

## Extending the System

### Replacing Mocked Components

- **CAD Parser**: Replace `ml_module/parser.py` mock implementation with actual STEP parser
- **OpenAI Integration**: Update `backend/src/main/java/com/cnc/tool/recommender/services/OpenAiService.java` to use real API calls
- **Speed/Feed Calculator**: Implement real algorithm in `backend/src/main/java/com/cnc/tool/recommender/services/SpeedFeedService.java`

### Adding New Features

- **Additional Tool Types**: Update `database/schema.sql` and tool model classes
- **New Geometric Features**: Extend classifier in `ml_module/classifier.py`
- **Enhanced Visualization**: Add 3D viewer component in frontend

## Project Structure

- `backend/`: Java Spring Boot application
- `frontend/`: React frontend
- `ml_module/`: Python classification and parsing modules
- `data/`: Sample data files and mock responses
- `database/`: Database schema and seed scripts
- `docs/`: Detailed documentation

## License

MIT 