# Backend Module

This module contains the Spring Boot backend for the CNC Tool Recommender system.

## Architecture

The backend is built using Spring Boot and provides RESTful APIs for:
- File upload and CAD feature extraction
- Machine and tool management
- Tool recommendations with speed and feed calculations
- Feedback collection and processing

## Key Components

- **Controllers**: Handle HTTP requests and responses
- **Services**: Implement business logic
- **Models**: Represent database entities and DTOs
- **Repositories**: Handle database operations
- **Utils**: Utility classes for common operations

## API Endpoints

Here are the main API endpoints:

### Health Check

- `GET /api/health`: Check system health

### CAD Files and Features

- `POST /api/cad-files`: Upload a CAD file
- `GET /api/cad-files`: Get all CAD files
- `GET /api/cad-files/{id}`: Get a CAD file by ID
- `GET /api/cad-files/{id}/features`: Get features for a CAD file

### Machines

- `GET /api/machines`: Get all machines
- `GET /api/machines/{id}`: Get a machine by ID

### Tools

- `GET /api/tools`: Get all tools
- `GET /api/tools/{id}`: Get a tool by ID

### Recommendations

- `POST /api/recommendations?cadFileId={id}&machineId={id}`: Generate tool recommendations
- `POST /api/recommendations/{id}/feedback?rating={rating}`: Submit feedback

## Setup Instructions

### Prerequisites

- Java 17 or higher
- Maven 3.6 or higher
- PostgreSQL database

### With Docker (Recommended)

The easiest way to run the backend is using Docker:

```bash
# From project root
docker-compose up -d backend
```

### Manual Setup

1. Configure database connection in `src/main/resources/application.properties`
2. Build the application:
   ```bash
   mvn clean install
   ```
3. Run the application:
   ```bash
   mvn spring-boot:run
   ```

### Environment Variables

The backend uses the following environment variables:

- `DB_HOST`: Database hostname (default: localhost)
- `DB_PORT`: Database port (default: 5432)
- `DB_NAME`: Database name (default: cnc_tool_recommender)
- `DB_USER`: Database username (default: postgres)
- `DB_PASSWORD`: Database password (default: password)
- `BACKEND_PORT`: Port for the backend server (default: 8080)
- `ML_MODULE_URL`: URL of the ML module (default: http://localhost:5050)
- `OPENAI_API_KEY`: OpenAI API key (for advanced features)
- `UPLOAD_DIR`: Directory for file uploads (default: ./uploads)

## Development Guide

### Adding a New API Endpoint

1. Create a controller method in the appropriate controller class
2. Implement required service methods
3. Create DTOs for request and response if needed
4. Add validation for request parameters
5. Document the endpoint with OpenAPI annotations

### Adding a New Entity

1. Create the entity class in the `models` package
2. Create a repository interface in the `repositories` package
3. Create a service class in the `services` package
4. Add DTOs for the entity if needed
5. Add mapping methods for converting between entity and DTOs

## Testing

Run the tests with:

```bash
mvn test
```

## API Documentation

Once the application is running, access the Swagger UI at:

```
http://localhost:8080/api/swagger-ui
```

This provides interactive documentation for all available endpoints.

## Building for Production

To build the application for production:

```bash
mvn clean package -DskipTests
```

The resulting JAR file will be in the `target` directory.

## Related Resources

For more information, check out:
- [Database Guide](../database.md) - Information about the database structure and data
- [Docker Guide](../docker_guide.md) - Guide to using Docker with this project
- [Debug Guide](../debug.md) - Tips for debugging common issues 