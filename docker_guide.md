# Docker Guide

This guide covers Docker usage for the CNC Tool Recommender system, including setup, common commands, best practices, and troubleshooting.

## Getting Started with Docker

Docker containers are used to ensure consistent development and deployment environments for the CNC Tool Recommender system.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### System Architecture

The CNC Tool Recommender system consists of the following Docker containers:

- **Frontend**: React application
- **Backend**: Spring Boot Java application
- **Database**: PostgreSQL database
- **Message Queue**: RabbitMQ for async operations (optional)
- **Recommendation Engine**: Python-based ML service

## Basic Commands

### Starting the System

```bash
# Start all services in detached mode
docker-compose up -d

# Start specific services
docker-compose up -d frontend backend postgres
```

### Stopping the System

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (will delete database data)
docker-compose down -v
```

### Checking Status

```bash
# View running containers
docker-compose ps

# View logs for all services
docker-compose logs

# View logs for a specific service
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f backend
```

### Accessing Containers

```bash
# Open a shell in a container
docker-compose exec backend bash

# Run a one-off command
docker-compose exec postgres psql -U postgres -d cnc_tool_recommender
```

## Development Workflow

### Building Images

```bash
# Rebuild all images
docker-compose build

# Rebuild a specific service
docker-compose build backend
```

### Development Mode

For development, you can mount local code into containers:

```bash
# In docker-compose.yml
services:
  backend:
    volumes:
      - ./backend:/app
```

### Hot Reloading

The frontend container is configured for hot reloading. Changes to local files will automatically update in the browser.

The backend may require rebuilding or restarting depending on the change:

```bash
# Restart a service
docker-compose restart backend
```

## Configuration

### Environment Variables

Environment variables are defined in:

1. `.env` file (for local development)
2. `docker-compose.yml` (for service configuration)

Key environment variables include:

```
# Database
DB_HOST=postgres
DB_PORT=5432
DB_NAME=cnc_tool_recommender
DB_USER=postgres
DB_PASSWORD=your_password

# API
API_PORT=8080
API_URL=http://localhost:8080

# Frontend
REACT_APP_API_URL=http://localhost:8080/api
```

### Volume Management

Data persistence is handled through Docker volumes:

```bash
# List volumes
docker volume ls

# Remove unused volumes
docker volume prune
```

## Best Practices

### Security Best Practices

1. **Never commit secrets to Git**
   - Use environment variables or Docker secrets
   - Keep `.env` files in `.gitignore`

2. **Use specific image versions**
   - Avoid `latest` tag to prevent unexpected changes

3. **Run containers with non-root users**
   - Set user in Dockerfile: `USER appuser`

4. **Scan images for vulnerabilities**
   - Use Docker Scout or similar tools

### Performance Optimization

1. **Optimize Dockerfiles**
   - Use multi-stage builds
   - Include only necessary files
   - Order instructions to maximize layer caching

2. **Separate development and production configurations**
   - Use docker-compose.override.yml for development-specific settings

3. **Resource constraints**
   - Set memory and CPU limits for containers

### Deployment Considerations

1. **Use container orchestration for production**
   - Kubernetes or Docker Swarm

2. **Implement health checks**
   - Add HEALTHCHECK instruction to Dockerfiles
   - Configure health checks in docker-compose.yml

3. **Set up proper logging**
   - Use a logging driver appropriate for your environment

## Common Issues and Solutions

### Container Won't Start

**Problem**: A container fails to start.

**Solutions**:
- Check logs: `docker-compose logs [service]`
- Verify port availability: `netstat -tulpn | grep [port]`
- Check environment variables: `docker-compose config`
- Ensure Docker has sufficient resources

### Database Connection Issues

**Problem**: Backend can't connect to database.

**Solutions**:
- Ensure database container is running: `docker-compose ps`
- Verify network connectivity: `docker-compose exec backend ping postgres`
- Check credentials and connection string
- Ensure database initialization completed

### Image Build Failures

**Problem**: Docker image fails to build.

**Solutions**:
- Check Dockerfile syntax
- Verify build context
- Ensure internet connectivity for package downloads
- Clean Docker cache: `docker builder prune`

### Volume Permission Issues

**Problem**: Permission denied when accessing mounted volumes.

**Solutions**:
- Set appropriate permissions on host directories
- Use Docker user mapping
- Fix ownership: `chown -R [uid]:[gid] [host_directory]`

## Docker Compose File Reference

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8080/api
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - SPRING_DATASOURCE_URL=jdbc:postgresql://postgres:5432/cnc_tool_recommender
      - SPRING_DATASOURCE_USERNAME=postgres
      - SPRING_DATASOURCE_PASSWORD=postgres
    depends_on:
      - postgres

  postgres:
    image: postgres:13
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=cnc_tool_recommender
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

## Advanced Docker Topics

### Docker Networking

The CNC Tool Recommender services communicate over a Docker bridge network created by Docker Compose.

To inspect the network:

```bash
docker network ls
docker network inspect e2e_default
```

### Custom Networks

For advanced setups, you can define custom networks:

```yaml
# In docker-compose.yml
networks:
  frontend-network:
  backend-network:

services:
  frontend:
    networks:
      - frontend-network
  
  backend:
    networks:
      - frontend-network
      - backend-network
  
  postgres:
    networks:
      - backend-network
```

### Docker Registry

For team development, consider using a private Docker registry:

```bash
# Push image to registry
docker tag cnc-tool-recommender-backend:latest registry.example.com/cnc-tool-recommender-backend:latest
docker push registry.example.com/cnc-tool-recommender-backend:latest

# Pull image from registry
docker pull registry.example.com/cnc-tool-recommender-backend:latest
```

## FAQ

### How do I update a single service?

```bash
# Pull latest code, rebuild and restart
git pull
docker-compose build backend
docker-compose up -d --no-deps backend
```

### How do I view container resource usage?

```bash
docker stats
```

### How do I debug a crashing container?

```bash
# Start with a shell instead of the default command
docker-compose run --rm backend bash

# Then run the application manually
java -jar app.jar
```

### How do I back up the database?

```bash
docker-compose exec postgres pg_dump -U postgres -d cnc_tool_recommender > backup.sql
```

### How do I restore a database backup?

```bash
cat backup.sql | docker-compose exec -T postgres psql -U postgres -d cnc_tool_recommender
```

### How do I add a new service?

Add a new section to your docker-compose.yml:

```yaml
recommendation-engine:
  build:
    context: ./recommendation-engine
    dockerfile: Dockerfile
  ports:
    - "5000:5000"
  depends_on:
    - backend
```

### How do I upgrade Docker Compose file version?

Check the [Docker Compose file reference](https://docs.docker.com/compose/compose-file/) for the latest syntax and update your docker-compose.yml accordingly.

## Docker Cheat Sheet

### Basic Commands
```
docker-compose up -d            # Start services
docker-compose down             # Stop services
docker-compose ps               # List containers
docker-compose logs             # View logs
docker-compose exec             # Run command in container
docker-compose build            # Build images
```

### Container Management
```
docker ps                       # List running containers
docker inspect [container]      # Container details
docker stats                    # Container resource usage
docker top [container]          # Running processes
```

### Image Management
```
docker images                   # List images
docker pull [image]             # Pull image
docker push [image]             # Push image to registry
docker rmi [image]              # Remove image
```

### Cleanup
```
docker system prune             # Remove unused data
docker volume prune             # Remove unused volumes
docker container prune          # Remove stopped containers
docker image prune              # Remove dangling images
``` 