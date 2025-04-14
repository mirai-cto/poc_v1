# Database Guide

This guide explains how to view and manage the PostgreSQL database for the CNC Tool Recommender system.

## Database Overview

The CNC Tool Recommender system uses PostgreSQL for data storage. The database contains tables for tools, materials, cutting parameters, and user preferences.

## Connection Information

### Local Development

```
Host: localhost
Port: 5432
Database: cnc_tool_recommender
Username: postgres
Password: See .env file or environment variables
```

### Docker Environment

When running with Docker, use the service name instead of localhost:

```
Host: postgres
Port: 5432
Database: cnc_tool_recommender
Username: postgres
Password: See docker-compose.yml or environment variables
```

## Connecting to the Database

### Using psql CLI

```bash
# Connect to local database
psql -h localhost -U postgres -d cnc_tool_recommender

# When using Docker
docker exec -it postgres psql -U postgres -d cnc_tool_recommender
```

### Using pgAdmin

1. Open pgAdmin in your browser (typically at http://localhost:5050 if running with Docker)
2. Register a new server:
   - Name: CNC Tool Recommender
   - Host: localhost (or postgres if connecting from within Docker network)
   - Port: 5432
   - Database: cnc_tool_recommender
   - Username: postgres
   - Password: (from environment variables)

## Common SQL Commands

### Viewing Tables

```sql
-- List all tables
\dt

-- Describe a specific table
\d+ tools

-- Show table contents
SELECT * FROM tools LIMIT 10;
```

### Querying Data

```sql
-- Basic SELECT query
SELECT id, name, diameter, material FROM tools WHERE tool_type = 'endmill';

-- JOIN example
SELECT t.name, m.name, cp.feed_rate, cp.speed
FROM tools t
JOIN materials m ON t.material_id = m.id
JOIN cutting_parameters cp ON t.id = cp.tool_id AND m.id = cp.material_id;

-- Group and aggregate data
SELECT tool_type, COUNT(*) as tool_count, AVG(diameter) as avg_diameter
FROM tools
GROUP BY tool_type;
```

### Modifying Data

```sql
-- Insert new tool
INSERT INTO tools (name, diameter, material, tool_type)
VALUES ('End Mill 10mm HSS', 10.0, 'HSS', 'endmill');

-- Update existing record
UPDATE tools
SET material = 'Carbide'
WHERE id = 1;

-- Delete record
DELETE FROM tools WHERE id = 5;
```

## Database Schema

### Main Tables

#### `tools` Table

Stores information about cutting tools.

| Column      | Type         | Description                    |
|-------------|--------------|--------------------------------|
| id          | SERIAL       | Primary key                    |
| name        | VARCHAR(255) | Tool name                      |
| diameter    | DECIMAL      | Tool diameter in mm            |
| length      | DECIMAL      | Tool length in mm              |
| flutes      | INTEGER      | Number of flutes               |
| material    | VARCHAR(100) | Tool material (HSS, Carbide)   |
| tool_type   | VARCHAR(100) | Type (endmill, drill, etc.)    |
| created_at  | TIMESTAMP    | Creation timestamp             |
| updated_at  | TIMESTAMP    | Last update timestamp          |

#### `materials` Table

Stores information about workpiece materials.

| Column      | Type         | Description                    |
|-------------|--------------|--------------------------------|
| id          | SERIAL       | Primary key                    |
| name        | VARCHAR(255) | Material name                  |
| category    | VARCHAR(100) | Category (steel, aluminum)     |
| hardness    | VARCHAR(100) | Hardness rating                |
| created_at  | TIMESTAMP    | Creation timestamp             |
| updated_at  | TIMESTAMP    | Last update timestamp          |

#### `cutting_parameters` Table

Stores recommended cutting parameters for tool/material combinations.

| Column      | Type         | Description                    |
|-------------|--------------|--------------------------------|
| id          | SERIAL       | Primary key                    |
| tool_id     | INTEGER      | Foreign key to tools           |
| material_id | INTEGER      | Foreign key to materials       |
| speed       | DECIMAL      | Cutting speed (RPM)            |
| feed_rate   | DECIMAL      | Feed rate (mm/min)             |
| doc         | DECIMAL      | Depth of cut (mm)              |
| created_at  | TIMESTAMP    | Creation timestamp             |
| updated_at  | TIMESTAMP    | Last update timestamp          |

### Relationships

- `cutting_parameters.tool_id` references `tools.id`
- `cutting_parameters.material_id` references `materials.id`

## Backing Up and Restoring Data

### Creating Database Backup

```bash
# Local backup
pg_dump -h localhost -U postgres -d cnc_tool_recommender > backup.sql

# Docker backup
docker exec -it postgres pg_dump -U postgres -d cnc_tool_recommender > backup.sql
```

### Restoring Database from Backup

```bash
# Local restore
psql -h localhost -U postgres -d cnc_tool_recommender < backup.sql

# Docker restore
cat backup.sql | docker exec -i postgres psql -U postgres -d cnc_tool_recommender
```

## Monitoring Database Performance

### Check Active Connections

```sql
SELECT * FROM pg_stat_activity;
```

### Get Table Sizes

```sql
SELECT
    table_name,
    pg_size_pretty(pg_total_relation_size(quote_ident(table_name))) as total_size
FROM
    information_schema.tables
WHERE
    table_schema = 'public'
ORDER BY
    pg_total_relation_size(quote_ident(table_name)) DESC;
```

### Check Indexes

```sql
SELECT
    indexname,
    indexdef
FROM
    pg_indexes
WHERE
    tablename = 'tools';
```

### Query Performance

```sql
-- Enable query timing
\timing

-- Run EXPLAIN ANALYZE on slow queries
EXPLAIN ANALYZE SELECT * FROM tools WHERE material = 'Carbide';
```

## Troubleshooting

### Common Issues

#### Connection Refused

**Problem:** Cannot connect to the database with error "connection refused"

**Solutions:**
- Check if PostgreSQL service is running
- Verify connection parameters (host, port)
- Check firewall settings

#### Permission Denied

**Problem:** "permission denied" error when connecting

**Solutions:**
- Verify username and password
- Check database user permissions

#### Slow Queries

**Problem:** Queries taking too long to execute

**Solutions:**
- Run EXPLAIN ANALYZE to identify bottlenecks
- Add indexes to frequently queried columns
- Optimize query structure
- Check for table bloat and run VACUUM

## Database Maintenance

### Regular Maintenance Tasks

```sql
-- Update statistics
ANALYZE;

-- Reclaim space and update statistics
VACUUM ANALYZE;

-- Full cleanup (locks tables - use during maintenance window)
VACUUM FULL;
```

### Add Indexes for Performance

```sql
-- Add index to frequently queried column
CREATE INDEX idx_tools_material ON tools(material);

-- Add composite index for multi-column queries
CREATE INDEX idx_cutting_params ON cutting_parameters(tool_id, material_id);
```

## Best Practices

1. **Use Parameterized Queries** - Always use parameterized queries in application code to prevent SQL injection

2. **Regular Backups** - Schedule regular database backups

3. **Version Control Schema Changes** - Use migration tools to version control schema changes

4. **Monitor Performance** - Set up monitoring for database performance metrics

5. **Indexing Strategy** - Create indexes for frequently queried columns, but avoid over-indexing

6. **Connection Pooling** - Use connection pooling in the application to manage database connections efficiently

7. **Security** - Restrict network access to the database and use strong passwords

8. **Regular Maintenance** - Schedule regular maintenance tasks like VACUUM and ANALYZE 