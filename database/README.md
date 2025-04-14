# Database Module

This module handles the database schema and data ingestion for the CNC Tool Recommender system.

## Contents

- `schema.sql`: PostgreSQL database schema definitions
- `seed.py`: Script for loading CSV data into the database
- `Dockerfile`: Container definition for the data seeder
- `requirements.txt`: Python dependencies for the seeder

## Database Schema

The database is structured around the following main entities:

1. **Machines**: Represents CNC machines with their specifications and limits
2. **Tools**: Represents cutting tools with their physical and operational characteristics
3. **CAD Files**: Stores information about uploaded CAD models
4. **CAD Features**: Geometric features extracted from CAD models
5. **CAD Feature Types**: Classification of geometric features (holes, slots, etc.)
6. **Recommended Tools**: Tool recommendations with speed and feed parameters
7. **Tool Usage Feedback**: User feedback on tool performance

## Data Ingestion

The `seed.py` script reads data from CSV files and populates the database tables:

- `machines.csv`: Contains machine specifications
- `tools.csv`: Contains tool specifications

The CSV files are expected to have column names matching the database schema.

## Setup Instructions

### With Docker (Recommended)

The database and seeder are configured to run with Docker Compose:

```bash
# From project root
docker-compose up -d db
docker-compose run --rm db_seeder
```

### Manual Setup

1. Create a PostgreSQL database:
   ```bash
   createdb cnc_tool_recommender
   ```

2. Apply the schema:
   ```bash
   psql -d cnc_tool_recommender -f schema.sql
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the seeder:
   ```bash
   python seed.py
   ```

## Extending the Database

### Adding New Tables

1. Update `schema.sql` with your new table definitions
2. Apply the changes to the database:
   ```bash
   psql -d cnc_tool_recommender -f schema.sql
   ```

### Adding New Data Sources

To add a new data source:

1. Add the CSV file to the `data/` directory
2. Create a new import function in `seed.py` following the pattern of existing functions
3. Call your new function from the `main()` function 