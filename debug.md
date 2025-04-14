# Debugging Guide

This guide provides comprehensive information on debugging the CNC Tool Recommender system, including best practices and solutions for common error scenarios.

## Table of Contents

- [General Debugging Approach](#general-debugging-approach)
- [Frontend Debugging](#frontend-debugging)
- [Backend Debugging](#backend-debugging)
- [Database Debugging](#database-debugging)
- [Docker Environment Debugging](#docker-environment-debugging)
- [Common Error Scenarios](#common-error-scenarios)
- [Performance Troubleshooting](#performance-troubleshooting)
- [Debugging Tools](#debugging-tools)

## General Debugging Approach

### Methodical Troubleshooting Process

1. **Identify the problem precisely**
   - What is happening vs. what should be happening?
   - Can you reproduce the issue consistently?
   - Which component is likely involved (frontend, backend, database)?

2. **Check the logs**
   - Frontend console logs
   - Backend application logs
   - Database logs
   - Docker container logs

3. **Isolate the issue**
   - Test components individually
   - Create minimal test cases
   - Disable features temporarily to narrow down the cause

4. **Test hypotheses systematically**
   - Make one change at a time
   - Document each attempted solution
   - Verify if the issue is resolved after each change

5. **Root cause analysis**
   - Identify underlying issues, not just symptoms
   - Document findings for future reference

### Effective Logging Practices

- Use appropriate log levels (DEBUG, INFO, WARN, ERROR)
- Include contextual information in log messages
- Log the beginning and end of important operations
- Include timestamps and correlation IDs
- Don't log sensitive information (passwords, tokens)

## Frontend Debugging

### Browser Developer Tools

#### Console
```javascript
// Log messages with different levels
console.log("Information message");
console.warn("Warning message");
console.error("Error message");

// Group related logs
console.group("User Authentication");
console.log("Checking credentials");
console.log("Setting tokens");
console.groupEnd();

// Timing operations
console.time("dataFetch");
fetchData().then(() => console.timeEnd("dataFetch"));
```

#### Network Tab
- Monitor API requests and responses
- Check HTTP status codes
- Examine request headers and payloads
- Verify response data
- Measure network performance

#### React DevTools
- Inspect component hierarchy
- Monitor state and props changes
- Check component rendering performance
- Test component interactions

### Common Frontend Issues

#### State Management Problems
- Inconsistent state updates
- Missing state synchronization
- Prop drilling issues
- Redux/context API misuse

#### Rendering Issues
- Infinite re-render loops
- Missing key props in lists
- Component lifecycle issues
- CSS/styling conflicts

#### API Integration Issues
- Incorrect endpoint URLs
- Missing headers or authentication
- Malformed request data
- Error handling gaps

## Backend Debugging

### Spring Boot Debugging

#### Enabling Debug Logs
```properties
# In application.properties
logging.level.root=INFO
logging.level.com.cnctoolrecommender=DEBUG
logging.level.org.springframework.web=DEBUG
```

#### Using Breakpoints
1. Set breakpoints in your IDE
2. Run the application in debug mode
3. Step through code execution
4. Inspect variables and call stack

#### Spring Boot Actuator
Enable Spring Boot Actuator endpoints for monitoring:

```properties
# In application.properties
management.endpoints.web.exposure.include=health,info,metrics,env
```

Access at:
- http://localhost:8080/actuator/health
- http://localhost:8080/actuator/info
- http://localhost:8080/actuator/metrics
- http://localhost:8080/actuator/env

### Common Backend Issues

#### API Endpoint Issues
- Request mapping conflicts
- Incorrect HTTP methods
- Missing @RequestBody or @PathVariable annotations
- Invalid payload validation

#### Database Connectivity
- Connection pool exhaustion
- Transaction management issues
- Incorrect SQL queries
- JPA/Hibernate configuration problems

#### Performance Issues
- N+1 query problems
- Missing database indexes
- Inefficient algorithms
- Memory leaks

## Database Debugging

### PostgreSQL Troubleshooting

#### Query Analysis
Use `EXPLAIN ANALYZE` to examine query execution:

```sql
EXPLAIN ANALYZE 
SELECT * FROM tools WHERE material_id = 5 AND tool_type = 'MILL';
```

#### Connection Issues
Check active connections:

```sql
SELECT * FROM pg_stat_activity;
```

#### Slow Query Diagnosis
Identify slow queries:

```sql
SELECT query, calls, total_time, rows, 
       mean_time, stddev_time, max_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

Enable pg_stat_statements extension if not enabled:

```sql
CREATE EXTENSION pg_stat_statements;
```

### Common Database Issues

#### Schema Problems
- Missing indexes
- Incorrect constraints
- Denormalization issues
- Data type mismatches

#### Performance Issues
- Table fragmentation
- Missing statistics
- Unoptimized queries
- Lock contention

## Docker Environment Debugging

### Container Debugging

#### Checking Container Logs
```bash
# View logs for a specific service
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f backend

# View a specific number of lines
docker-compose logs --tail=100 backend
```

#### Inspecting Running Containers
```bash
# View detailed container information
docker inspect <container_id>

# Check container resources
docker stats <container_id>

# Execute commands inside containers
docker exec -it <container_id> bash
```

### Common Docker Issues

#### Container Startup Failures
- Missing environment variables
- Volume mount issues
- Port conflicts
- Resource constraints

#### Inter-service Communication
- Network configuration problems
- Service discovery issues
- Hostname resolution failures
- Timing/race conditions during startup

## Common Error Scenarios

### 1. Frontend Cannot Connect to Backend API

**Symptoms:**
- Network errors in browser console
- "Failed to fetch" errors
- CORS errors

**Troubleshooting Steps:**
1. Verify backend service is running: `docker-compose ps`
2. Check backend logs for errors: `docker-compose logs backend`
3. Confirm API URL configuration in frontend
4. Verify network settings in docker-compose.yml
5. Check for CORS configuration on backend
6. Test API endpoint directly with curl or Postman

**Common Solutions:**
```java
// In backend Spring Boot application
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            .allowedOrigins("http://localhost:3000")
            .allowedMethods("GET", "POST", "PUT", "DELETE")
            .allowCredentials(true);
    }
}
```

### 2. Database Connection Failures

**Symptoms:**
- "Could not connect to database" errors in backend logs
- Connection timeout errors
- "Connection refused" messages

**Troubleshooting Steps:**
1. Verify database container is running: `docker-compose ps`
2. Check database logs: `docker-compose logs postgres`
3. Confirm database credentials in application.properties
4. Test database connection directly: 
   ```bash
   docker exec -it <postgres_container_id> psql -U postgres -d cnc_tool_recommender
   ```
5. Check network settings in docker-compose.yml

**Common Solutions:**
```properties
# Correct Spring Boot database configuration
spring.datasource.url=jdbc:postgresql://postgres:5432/cnc_tool_recommender
spring.datasource.username=postgres
spring.datasource.password=postgres
spring.datasource.driver-class-name=org.postgresql.Driver
```

### 3. Missing Data in Tool Recommendations

**Symptoms:**
- Empty recommendation results
- Missing tools in listings
- Incorrect filtering behavior

**Troubleshooting Steps:**
1. Check database for expected data:
   ```sql
   SELECT * FROM tools WHERE material_id = ?;
   SELECT * FROM cutting_parameters WHERE tool_id = ? AND material_id = ?;
   ```
2. Verify query logic in service layer
3. Check for transaction issues or caching problems
4. Validate request parameters from frontend
5. Test recommendation algorithm independently

**Common Solutions:**
- Review repository methods for correct query conditions
- Check service layer business logic
- Verify data transformation/mapping
- Check for NULL handling in queries

### 4. Performance Degradation

**Symptoms:**
- Slow page loading
- Delayed API responses
- High CPU/memory usage

**Troubleshooting Steps:**
1. Identify bottlenecks using profiling tools
2. Check database query performance
3. Monitor resource usage: `docker stats`
4. Review frontend rendering performance
5. Check for memory leaks

**Common Solutions:**
- Optimize database queries and add indexes
- Implement caching where appropriate
- Review frontend component rendering
- Check for unnecessary re-renders in React
- Optimize Docker resource allocations

### 5. Authentication/Authorization Issues

**Symptoms:**
- Unauthorized errors (HTTP 401)
- Forbidden errors (HTTP 403)
- User session problems

**Troubleshooting Steps:**
1. Check token validity and expiration
2. Verify user roles and permissions
3. Review security configuration
4. Check for proper token transmission in requests
5. Validate token signing and verification

**Common Solutions:**
```java
// Example token verification debugging
@Component
public class JwtTokenUtil {
    private static final Logger logger = LoggerFactory.getLogger(JwtTokenUtil.class);
    
    public boolean validateToken(String token) {
        try {
            // Token validation logic
            return true;
        } catch (ExpiredJwtException e) {
            logger.error("JWT token expired: {}", e.getMessage());
        } catch (UnsupportedJwtException e) {
            logger.error("Unsupported JWT token: {}", e.getMessage());
        } catch (MalformedJwtException e) {
            logger.error("Malformed JWT: {}", e.getMessage());
        } catch (Exception e) {
            logger.error("Token validation error: {}", e.getMessage());
        }
        return false;
    }
}
```

## Performance Troubleshooting

### Frontend Performance

#### React Component Profiling
Use React DevTools Profiler to:
- Record rendering performance
- Identify components causing slowdowns
- Detect unnecessary re-renders

#### Bundle Size Analysis
```bash
# Install source-map-explorer
npm install -g source-map-explorer

# Analyze bundle
source-map-explorer build/static/js/main.*.js
```

#### Render Optimization
- Implement React.memo for pure components
- Use useCallback and useMemo hooks
- Virtualize long lists with react-window
- Lazy load components and routes

### Backend Performance

#### JVM Profiling
Use tools like VisualVM, JProfiler, or YourKit to:
- Monitor memory usage
- Detect memory leaks
- Analyze CPU hotspots
- Track thread activity

#### Database Query Optimization
- Add appropriate indexes
- Optimize JOIN operations
- Use query hints where necessary
- Consider materialized views for complex queries

#### Caching Strategies
- Implement Spring Cache
- Use Redis for distributed caching
- Consider browser caching for static assets
- Add entity-level caching in Hibernate

## Debugging Tools

### Recommended Tools

#### Development Tools
- IntelliJ IDEA / VS Code with debugger extensions
- Chrome/Firefox DevTools
- Postman or Insomnia for API testing
- DBeaver or pgAdmin for database management

#### Monitoring & Profiling
- Prometheus for metrics collection
- Grafana for dashboard visualization
- Spring Boot Actuator for application metrics
- PostgreSQL pg_stat_statements for query analysis

#### Logging Tools
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Papertrail for centralized logging
- Sentry for error tracking
- Log4j2/Logback for backend logging

### Setting Up Local Debug Environment

1. **Enable Remote Debugging for Java Applications**

   In docker-compose.yml:
   ```yaml
   services:
     backend:
       environment:
         - JAVA_TOOL_OPTIONS=-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005
       ports:
         - "8080:8080"
         - "5005:5005"  # Debug port
   ```

2. **Configure IDE for Remote Debugging**

   For IntelliJ IDEA:
   - Go to Run > Edit Configurations
   - Add a new Remote JVM Debug configuration
   - Set host to localhost and port to 5005
   - Start the debug session

3. **Enable Source Maps for Frontend**

   In webpack configuration:
   ```javascript
   module.exports = {
     // ... other config
     devtool: 'source-map'
   };
   ```

## Conclusion

Effective debugging is a combination of systematic problem-solving, proper logging, understanding the system architecture, and using the right tools. By following the approaches outlined in this guide, you can efficiently identify and resolve issues in the CNC Tool Recommender system.

Remember that good debugging practices begin with good development practices:
- Write testable code
- Implement comprehensive logging
- Use consistent error handling
- Create meaningful documentation
- Follow established patterns and conventions

For specific issues not covered in this guide, consult the project's internal documentation or reach out to the development team for assistance. 