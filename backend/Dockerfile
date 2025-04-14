FROM maven:3.9.6-eclipse-temurin-17 AS build

WORKDIR /app

# Copy pom.xml
COPY pom.xml .

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application
RUN mvn package -DskipTests

# Create runtime image
FROM eclipse-temurin:17-jre-jammy

WORKDIR /app

# Copy the built JAR file
COPY --from=build /app/target/*.jar app.jar

# Create uploads directory
RUN mkdir -p uploads

# Set environment variables
ENV SPRING_PROFILES_ACTIVE=prod

# Expose the application port
EXPOSE 8080

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"] 