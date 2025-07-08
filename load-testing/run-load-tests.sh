#!/bin/bash


set -e

echo "=========================================="
echo "Model Registry Load Testing Script"
echo "=========================================="

echo "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is required but not installed."
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is required but not installed."
    exit 1
fi

echo "Installing required Python packages..."
pip3 install requests matplotlib pandas psutil

if command -v jmeter &> /dev/null; then
    echo "JMeter found - will run JMeter tests"
    JMETER_AVAILABLE=true
else
    echo "JMeter not found - skipping JMeter tests (install JMeter for additional testing)"
    JMETER_AVAILABLE=false
fi

echo "Creating results directories..."
mkdir -p /home/ubuntu/devin-iris-rahul2/load-testing/results
mkdir -p /home/ubuntu/devin-iris-rahul2/load-testing/reports

echo "Checking if backend server is running..."
if ! curl -s http://localhost:8080/api/load-test/database-stats > /dev/null; then
    echo "ERROR: Backend server is not running on localhost:8080"
    echo "Please start the Spring Boot application first:"
    echo "  cd /home/ubuntu/devin-iris-rahul2/backend"
    echo "  ./mvnw spring-boot:run"
    exit 1
fi

echo "Backend server is running ✓"

echo "Getting current database statistics..."
CURRENT_COUNT=$(curl -s http://localhost:8080/api/load-test/database-stats | python3 -c "import sys, json; print(json.load(sys.stdin)['modelCount'])")
echo "Current model count: $CURRENT_COUNT"

if [ "$CURRENT_COUNT" -lt 1000000 ]; then
    echo ""
    echo "WARNING: Database currently has $CURRENT_COUNT records."
    echo "Load testing requires 1 million records for accurate performance measurement."
    echo ""
    read -p "Do you want to generate 1 million records? This will take several minutes. (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Generating 1 million records..."
        echo "This may take 10-15 minutes depending on system performance..."
        
        START_TIME=$(date +%s)
        
        curl -X POST http://localhost:8080/api/load-test/generate-million \
             -H "Content-Type: application/json" \
             -w "\nHTTP Status: %{http_code}\nTotal Time: %{time_total}s\n"
        
        END_TIME=$(date +%s)
        GENERATION_TIME=$((END_TIME - START_TIME))
        
        echo "Data generation completed in $GENERATION_TIME seconds"
        
        NEW_COUNT=$(curl -s http://localhost:8080/api/load-test/database-stats | python3 -c "import sys, json; print(json.load(sys.stdin)['modelCount'])")
        echo "New model count: $NEW_COUNT"
        
        if [ "$NEW_COUNT" -ge 1000000 ]; then
            echo "✓ Successfully generated 1 million records"
        else
            echo "⚠ Warning: Expected 1 million records but got $NEW_COUNT"
        fi
    else
        echo "Skipping data generation. Running tests with existing $CURRENT_COUNT records."
    fi
else
    echo "✓ Database already has sufficient records ($CURRENT_COUNT) for load testing"
fi

echo ""
echo "Running Python performance tests..."
cd /home/ubuntu/devin-iris-rahul2/load-testing
python3 performance-test-script.py

if [ "$JMETER_AVAILABLE" = true ]; then
    echo ""
    echo "Running JMeter load tests..."
    jmeter -n -t jmeter-test-plan.jmx -l results/jmeter-results-$(date +%Y%m%d_%H%M%S).jtl
    echo "JMeter tests completed"
fi

echo ""
echo "=========================================="
echo "Load Testing Summary"
echo "=========================================="

FINAL_COUNT=$(curl -s http://localhost:8080/api/load-test/database-stats | python3 -c "import sys, json; print(json.load(sys.stdin)['modelCount'])")
echo "Final database record count: $FINAL_COUNT"

echo "Test results saved in: /home/ubuntu/devin-iris-rahul2/load-testing/results/"
echo "Performance reports saved in: /home/ubuntu/devin-iris-rahul2/load-testing/reports/"

echo ""
echo "Generated reports:"
ls -la /home/ubuntu/devin-iris-rahul2/load-testing/reports/

echo ""
echo "Load testing completed successfully!"
echo "Review the generated HTML reports for detailed performance analysis."
