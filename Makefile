.PHONY: setup start stop clean build build-frontend build-backend setup-db seed-db test

# Setup the project
setup:
	cp .env.example .env
	@echo "Please update .env file with your OpenAI API key and other settings"
	docker-compose build

# Start all services
start:
	docker-compose up

# Start in detached mode
start-detached:
	docker-compose up -d

# Stop all services
stop:
	docker-compose down

# Clean up containers and volumes
clean:
	docker-compose down -v
	rm -rf uploads/*

# Build all services
build:
	docker-compose build

# Build frontend only
build-frontend:
	docker-compose build frontend

# Build backend only
build-backend:
	docker-compose build backend

# Setup the database
setup-db:
	docker-compose up -d db
	docker-compose run --rm db_seeder

# Seed the database with sample data
seed-db:
	docker-compose run --rm db_seeder

# Run tests
test:
	docker-compose run --rm backend ./mvnw test
	cd frontend && npm test

# Show logs
logs:
	docker-compose logs -f

# Direct access to database
db-shell:
	docker-compose exec db psql -U postgres -d cnc_tool_recommender

# Helper to check system status
status:
	@echo "Docker containers status:"
	@docker-compose ps 