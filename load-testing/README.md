# Load Testing for Model Registration and Inventory Management System

This directory contains comprehensive load testing tools and scripts for testing the Model Registration and Inventory Management System with 1 million records.

## Overview

The load testing framework tests the application's performance under realistic conditions with a large dataset, focusing on:

- **Pagination Performance**: Testing page navigation with large datasets
- **Search Functionality**: Testing search across all model attributes
- **Sorting Performance**: Testing sorting by different columns
- **CRUD Operations**: Testing create, read, update operations under load
- **Concurrent Users**: Testing system behavior with multiple simultaneous users

## Files

### Core Testing Files

- `performance-test-script.py` - Python-based performance testing script with detailed metrics
- `jmeter-test-plan.jmx` - JMeter test plan for comprehensive load testing
- `run-load-tests.sh` - Automated script to run all load tests

### Generated Directories

- `results/` - Raw test results and JMeter output files
- `reports/` - Generated HTML performance reports with charts and analysis

## Prerequisites

### Required Software

1. **Python 3** with pip
2. **MySQL** database running
3. **Spring Boot backend** running on localhost:8080
4. **Angular frontend** running on localhost:4200 (optional for UI testing)

### Required Python Packages

```bash
pip3 install requests matplotlib pandas psutil
```

### Optional: JMeter

Install Apache JMeter for additional load testing capabilities:

```bash
# Ubuntu/Debian
sudo apt-get install jmeter

# macOS
brew install jmeter
```

## Usage

### Quick Start

1. **Start the backend application:**
   ```bash
   cd /home/ubuntu/devin-iris-rahul2/backend
   ./mvnw spring-boot:run
   ```

2. **Run the automated load testing script:**
   ```bash
   cd /home/ubuntu/devin-iris-rahul2/load-testing
   chmod +x run-load-tests.sh
   ./run-load-tests.sh
   ```

3. **Review the generated reports** in the `reports/` directory

### Manual Testing

#### Generate Test Data

```bash
# Generate 1 million records
curl -X POST http://localhost:8080/api/load-test/generate-million

# Generate smaller sample (e.g., 10,000 records)
curl -X POST http://localhost:8080/api/load-test/generate-sample/10000

# Check database statistics
curl http://localhost:8080/api/load-test/database-stats
```

#### Run Python Performance Tests

```bash
python3 performance-test-script.py
```

#### Run JMeter Tests

```bash
jmeter -n -t jmeter-test-plan.jmx -l results/jmeter-results.jtl
```

## Test Scenarios

### 1. Pagination Performance Tests

Tests pagination with different page sizes and positions:

- Page 1 with 10, 20, 30 items per page
- Random pages (1000, 5000, 10000+) to test deep pagination
- Measures response times and success rates

### 2. Search Performance Tests

Tests search functionality across all model attributes:

- Common search terms: "Credit", "Market", "Risk", "Model", "Engine", "Calculator"
- Tests search with pagination
- Measures search response times and result accuracy

### 3. Sorting Performance Tests

Tests sorting by different columns:

- Model Name (ascending/descending)
- Created Date (ascending/descending)
- Business Line (ascending/descending)
- Status (ascending/descending)

### 4. CRUD Operations Tests

Tests create, read, update operations:

- Model creation with various attributes
- Individual model retrieval by ID
- Model updates with different field changes

### 5. Concurrent Load Tests

Tests system behavior under concurrent load:

- 10-50 concurrent users
- Multiple requests per user
- Measures throughput (requests per second)
- Monitors success rates under load

## Performance Metrics

The testing framework collects comprehensive metrics:

### Response Time Metrics
- Average response time
- Minimum response time
- Maximum response time
- Median response time
- 95th percentile (P95)
- 99th percentile (P99)

### Throughput Metrics
- Requests per second
- Successful requests
- Failed requests
- Success rate percentage

### System Resource Metrics
- CPU utilization
- Memory usage
- Disk usage
- Database connection pool status

## Generated Reports

### HTML Performance Report

The main performance report (`performance_report_YYYYMMDD_HHMMSS.html`) includes:

- **Executive Summary**: Overall performance metrics
- **Database Statistics**: Record counts and database health
- **API Performance Results**: Detailed test results table
- **Performance Recommendations**: Optimization suggestions
- **Test Environment**: Configuration details

### JMeter Reports

JMeter generates additional reports:

- Response time graphs
- Throughput over time
- Error rate analysis
- Concurrent user performance

## Performance Optimization Recommendations

Based on load testing results, consider these optimizations:

### Database Optimizations
- **Indexing**: Ensure proper indexes on frequently queried columns
- **Connection Pooling**: Optimize database connection pool settings
- **Query Optimization**: Review and optimize slow queries

### Application Optimizations
- **Caching**: Implement Redis caching for lookup data
- **Pagination**: Consider cursor-based pagination for very large datasets
- **API Rate Limiting**: Implement rate limiting to prevent overload

### Frontend Optimizations
- **Virtual Scrolling**: Implement virtual scrolling for large result sets
- **Lazy Loading**: Load data on demand
- **Client-side Caching**: Cache frequently accessed data

## Troubleshooting

### Common Issues

1. **Backend Not Running**
   ```
   ERROR: Backend server is not responding
   ```
   **Solution**: Start the Spring Boot application on localhost:8080

2. **Database Connection Issues**
   ```
   ERROR: Cannot connect to database
   ```
   **Solution**: Ensure MySQL is running and accessible

3. **Memory Issues During Data Generation**
   ```
   OutOfMemoryError during data generation
   ```
   **Solution**: Increase JVM heap size or generate data in smaller batches

4. **Slow Performance**
   ```
   Tests taking too long to complete
   ```
   **Solution**: Check database indexes and system resources

### Performance Thresholds

Consider these performance thresholds for evaluation:

- **Excellent**: < 100ms average response time
- **Good**: 100-500ms average response time
- **Acceptable**: 500ms-2s average response time
- **Poor**: > 2s average response time

- **Success Rate**: Should be > 95% for production readiness

## Data Cleanup

To clean up test data after testing:

```bash
# Clear all model data
curl -X DELETE http://localhost:8080/api/load-test/clear-data

# Verify cleanup
curl http://localhost:8080/api/load-test/database-stats
```

## Contributing

When adding new load tests:

1. Add test scenarios to `performance-test-script.py`
2. Update JMeter test plan if needed
3. Document new test cases in this README
4. Update performance thresholds if necessary

## Support

For issues or questions about load testing:

1. Check the generated error logs in `results/`
2. Review the performance reports for bottlenecks
3. Verify system requirements and prerequisites
4. Check database and application logs for errors
