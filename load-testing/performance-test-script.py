#!/usr/bin/env python3
"""
Performance Testing Script for Model Registration and Inventory Management System
Tests application performance with 1 million records
"""

import requests
import time
import json
import statistics
import concurrent.futures
import psutil
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os
import sys

class PerformanceTester:
    def __init__(self, base_url="http://localhost:8080", frontend_url="http://localhost:4200"):
        self.base_url = base_url
        self.frontend_url = frontend_url
        self.results = {
            'api_tests': [],
            'database_stats': {},
            'system_metrics': [],
            'test_summary': {}
        }
        
    def test_api_endpoint(self, endpoint, method="GET", data=None, params=None, iterations=10):
        """Test a single API endpoint multiple times and collect metrics"""
        print(f"Testing {method} {endpoint} ({iterations} iterations)...")
        
        response_times = []
        success_count = 0
        error_count = 0
        
        for i in range(iterations):
            start_time = time.time()
            
            try:
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}", params=params, timeout=30)
                elif method == "POST":
                    response = requests.post(f"{self.base_url}{endpoint}", json=data, timeout=30)
                elif method == "PUT":
                    response = requests.put(f"{self.base_url}{endpoint}", json=data, timeout=30)
                
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                
                if response.status_code < 400:
                    success_count += 1
                    response_times.append(response_time)
                else:
                    error_count += 1
                    print(f"Error {response.status_code}: {response.text}")
                    
            except Exception as e:
                error_count += 1
                print(f"Request failed: {str(e)}")
                
        if response_times:
            result = {
                'endpoint': endpoint,
                'method': method,
                'iterations': iterations,
                'success_count': success_count,
                'error_count': error_count,
                'success_rate': (success_count / iterations) * 100,
                'avg_response_time': statistics.mean(response_times),
                'min_response_time': min(response_times),
                'max_response_time': max(response_times),
                'median_response_time': statistics.median(response_times),
                'p95_response_time': self.percentile(response_times, 95),
                'p99_response_time': self.percentile(response_times, 99)
            }
        else:
            result = {
                'endpoint': endpoint,
                'method': method,
                'iterations': iterations,
                'success_count': 0,
                'error_count': error_count,
                'success_rate': 0,
                'avg_response_time': 0,
                'min_response_time': 0,
                'max_response_time': 0,
                'median_response_time': 0,
                'p95_response_time': 0,
                'p99_response_time': 0
            }
            
        self.results['api_tests'].append(result)
        return result
        
    def percentile(self, data, percentile):
        """Calculate percentile of a list"""
        if not data:
            return 0
        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)
        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower = sorted_data[int(index)]
            upper = sorted_data[int(index) + 1]
            return lower + (upper - lower) * (index - int(index))
            
    def concurrent_load_test(self, endpoint, concurrent_users=50, requests_per_user=10, params=None):
        """Run concurrent load test on an endpoint"""
        print(f"Running concurrent load test: {concurrent_users} users, {requests_per_user} requests each...")
        
        def make_request():
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}{endpoint}", params=params, timeout=30)
                end_time = time.time()
                return {
                    'response_time': (end_time - start_time) * 1000,
                    'status_code': response.status_code,
                    'success': response.status_code < 400
                }
            except Exception as e:
                return {
                    'response_time': 0,
                    'status_code': 0,
                    'success': False,
                    'error': str(e)
                }
        
        all_requests = []
        for _ in range(concurrent_users):
            all_requests.extend([make_request for _ in range(requests_per_user)])
        
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            results = list(executor.map(lambda f: f(), all_requests))
        
        end_time = time.time()
        total_time = end_time - start_time
        
        successful_requests = [r for r in results if r['success']]
        failed_requests = [r for r in results if not r['success']]
        
        if successful_requests:
            response_times = [r['response_time'] for r in successful_requests]
            
            load_test_result = {
                'endpoint': endpoint,
                'concurrent_users': concurrent_users,
                'requests_per_user': requests_per_user,
                'total_requests': len(results),
                'successful_requests': len(successful_requests),
                'failed_requests': len(failed_requests),
                'success_rate': (len(successful_requests) / len(results)) * 100,
                'total_time': total_time,
                'requests_per_second': len(results) / total_time,
                'avg_response_time': statistics.mean(response_times),
                'min_response_time': min(response_times),
                'max_response_time': max(response_times),
                'p95_response_time': self.percentile(response_times, 95),
                'p99_response_time': self.percentile(response_times, 99)
            }
        else:
            load_test_result = {
                'endpoint': endpoint,
                'concurrent_users': concurrent_users,
                'requests_per_user': requests_per_user,
                'total_requests': len(results),
                'successful_requests': 0,
                'failed_requests': len(failed_requests),
                'success_rate': 0,
                'total_time': total_time,
                'requests_per_second': 0,
                'avg_response_time': 0,
                'min_response_time': 0,
                'max_response_time': 0,
                'p95_response_time': 0,
                'p99_response_time': 0
            }
            
        return load_test_result
        
    def monitor_system_resources(self, duration=60):
        """Monitor system resources for a specified duration"""
        print(f"Monitoring system resources for {duration} seconds...")
        
        metrics = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            metrics.append({
                'timestamp': time.time(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_used_gb': memory.used / (1024**3),
                'memory_available_gb': memory.available / (1024**3),
                'disk_percent': disk.percent
            })
            
        self.results['system_metrics'] = metrics
        return metrics
        
    def get_database_stats(self):
        """Get database statistics"""
        try:
            response = requests.get(f"{self.base_url}/api/load-test/database-stats", timeout=30)
            if response.status_code == 200:
                self.results['database_stats'] = response.json()
                return response.json()
            else:
                print(f"Failed to get database stats: {response.status_code}")
                return {}
        except Exception as e:
            print(f"Error getting database stats: {str(e)}")
            return {}
            
    def run_comprehensive_tests(self):
        """Run comprehensive performance tests"""
        print("Starting comprehensive performance tests...")
        
        print("\n=== Database Statistics ===")
        db_stats = self.get_database_stats()
        print(f"Model count: {db_stats.get('modelCount', 'Unknown')}")
        print(f"Total lookup records: {db_stats.get('totalLookupRecords', 'Unknown')}")
        
        print("\n=== Testing Pagination Performance ===")
        pagination_tests = [
            {'page': 0, 'size': 10},
            {'page': 0, 'size': 20},
            {'page': 0, 'size': 30},
            {'page': 1000, 'size': 10},
            {'page': 5000, 'size': 20},
            {'page': 10000, 'size': 30}
        ]
        
        for params in pagination_tests:
            self.test_api_endpoint("/api/models", params=params, iterations=5)
            
        print("\n=== Testing Search Performance ===")
        search_terms = ["Credit", "Market", "Risk", "Model", "Engine", "Calculator"]
        for term in search_terms:
            params = {'search': term, 'page': 0, 'size': 20}
            self.test_api_endpoint("/api/models", params=params, iterations=5)
            
        print("\n=== Testing Sorting Performance ===")
        sort_tests = [
            {'sortBy': 'modelName', 'sortDirection': 'asc', 'page': 0, 'size': 20},
            {'sortBy': 'createdAt', 'sortDirection': 'desc', 'page': 0, 'size': 20},
            {'sortBy': 'businessLine', 'sortDirection': 'asc', 'page': 0, 'size': 20},
            {'sortBy': 'status', 'sortDirection': 'desc', 'page': 0, 'size': 20}
        ]
        
        for params in sort_tests:
            self.test_api_endpoint("/api/models", params=params, iterations=5)
            
        print("\n=== Testing CRUD Operations ===")
        sample_model = {
            "modelName": "Performance Test Model",
            "modelVersion": "v1.0.0",
            "modelSponsor": "Performance Tester",
            "businessLine": "RETAIL_BANKING",
            "modelType": "CREDIT_RISK",
            "riskRating": "MEDIUM",
            "status": "IN_DEVELOPMENT"
        }
        
        self.test_api_endpoint("/api/models", method="POST", data=sample_model, iterations=5)
        self.test_api_endpoint("/api/models/1", method="GET", iterations=5)
        
        print("\n=== Running Concurrent Load Tests ===")
        load_test_scenarios = [
            {'endpoint': '/api/models', 'concurrent_users': 10, 'requests_per_user': 5, 'params': {'page': 0, 'size': 10}},
            {'endpoint': '/api/models', 'concurrent_users': 25, 'requests_per_user': 4, 'params': {'page': 1000, 'size': 20}},
            {'endpoint': '/api/models', 'concurrent_users': 50, 'requests_per_user': 2, 'params': {'search': 'Credit', 'page': 0, 'size': 20}}
        ]
        
        for scenario in load_test_scenarios:
            result = self.concurrent_load_test(**scenario)
            print(f"Load test result: {result['requests_per_second']:.2f} req/sec, {result['success_rate']:.1f}% success rate")
            
        print("\nPerformance tests completed!")
        
    def generate_report(self, output_file="performance_report.html"):
        """Generate comprehensive performance report"""
        print(f"Generating performance report: {output_file}")
        
        if self.results['api_tests']:
            avg_response_times = [test['avg_response_time'] for test in self.results['api_tests']]
            success_rates = [test['success_rate'] for test in self.results['api_tests']]
            
            summary = {
                'total_tests': len(self.results['api_tests']),
                'overall_avg_response_time': statistics.mean(avg_response_times),
                'overall_success_rate': statistics.mean(success_rates),
                'fastest_response': min([test['min_response_time'] for test in self.results['api_tests']]),
                'slowest_response': max([test['max_response_time'] for test in self.results['api_tests']])
            }
            
            self.results['test_summary'] = summary
        
        html_content = self._generate_html_report()
        
        with open(output_file, 'w') as f:
            f.write(html_content)
            
        print(f"Performance report generated: {output_file}")
        return output_file
        
    def _generate_html_report(self):
        """Generate HTML content for the performance report"""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Model Registry Performance Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
        .section { margin: 20px 0; }
        .metric { background-color: #e8f4fd; padding: 10px; margin: 5px 0; border-radius: 3px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .success { color: green; }
        .warning { color: orange; }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Model Registration and Inventory Management System</h1>
        <h2>Performance Test Report with 1 Million Records</h2>
        <p>Generated on: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    </div>
    
    <div class="section">
        <h3>Executive Summary</h3>
        <div class="metric">Total Tests Executed: """ + str(self.results['test_summary'].get('total_tests', 0)) + """</div>
        <div class="metric">Overall Average Response Time: """ + f"{self.results['test_summary'].get('overall_avg_response_time', 0):.2f}" + """ ms</div>
        <div class="metric">Overall Success Rate: """ + f"{self.results['test_summary'].get('overall_success_rate', 0):.1f}" + """%</div>
        <div class="metric">Fastest Response: """ + f"{self.results['test_summary'].get('fastest_response', 0):.2f}" + """ ms</div>
        <div class="metric">Slowest Response: """ + f"{self.results['test_summary'].get('slowest_response', 0):.2f}" + """ ms</div>
    </div>
    
    <div class="section">
        <h3>Database Statistics</h3>
        <div class="metric">Model Records: """ + str(self.results['database_stats'].get('modelCount', 'Unknown')) + """</div>
        <div class="metric">Business Lines: """ + str(self.results['database_stats'].get('businessLineCount', 'Unknown')) + """</div>
        <div class="metric">Model Types: """ + str(self.results['database_stats'].get('modelTypeCount', 'Unknown')) + """</div>
        <div class="metric">Risk Ratings: """ + str(self.results['database_stats'].get('riskRatingCount', 'Unknown')) + """</div>
        <div class="metric">Statuses: """ + str(self.results['database_stats'].get('statusCount', 'Unknown')) + """</div>
    </div>
    
    <div class="section">
        <h3>API Performance Test Results</h3>
        <table>
            <tr>
                <th>Endpoint</th>
                <th>Method</th>
                <th>Iterations</th>
                <th>Success Rate</th>
                <th>Avg Response (ms)</th>
                <th>Min Response (ms)</th>
                <th>Max Response (ms)</th>
                <th>P95 Response (ms)</th>
                <th>P99 Response (ms)</th>
            </tr>
"""
        
        for test in self.results['api_tests']:
            success_class = "success" if test['success_rate'] >= 95 else "warning" if test['success_rate'] >= 80 else "error"
            html += f"""
            <tr>
                <td>{test['endpoint']}</td>
                <td>{test['method']}</td>
                <td>{test['iterations']}</td>
                <td class="{success_class}">{test['success_rate']:.1f}%</td>
                <td>{test['avg_response_time']:.2f}</td>
                <td>{test['min_response_time']:.2f}</td>
                <td>{test['max_response_time']:.2f}</td>
                <td>{test['p95_response_time']:.2f}</td>
                <td>{test['p99_response_time']:.2f}</td>
            </tr>
"""
        
        html += """
        </table>
    </div>
    
    <div class="section">
        <h3>Performance Recommendations</h3>
        <ul>
            <li><strong>Database Indexing:</strong> Ensure proper indexes on frequently queried columns (model_name, created_at, business_line_id, etc.)</li>
            <li><strong>Pagination Optimization:</strong> Consider using cursor-based pagination for very large datasets</li>
            <li><strong>Caching Strategy:</strong> Implement Redis caching for frequently accessed lookup data</li>
            <li><strong>Connection Pooling:</strong> Optimize database connection pool settings for high concurrency</li>
            <li><strong>Frontend Optimization:</strong> Implement virtual scrolling for large result sets</li>
            <li><strong>API Rate Limiting:</strong> Consider implementing rate limiting to prevent system overload</li>
        </ul>
    </div>
    
    <div class="section">
        <h3>Test Environment</h3>
        <div class="metric">Backend URL: """ + self.base_url + """</div>
        <div class="metric">Frontend URL: """ + self.frontend_url + """</div>
        <div class="metric">Database: MySQL with 1 million model records</div>
        <div class="metric">Test Framework: Python with requests library</div>
    </div>
    
</body>
</html>
"""
        return html

def main():
    """Main function to run performance tests"""
    print("Model Registry Performance Testing Script")
    print("=========================================")
    
    tester = PerformanceTester()
    
    try:
        response = requests.get(f"{tester.base_url}/api/load-test/database-stats", timeout=10)
        if response.status_code != 200:
            print("ERROR: Backend server is not responding. Please start the Spring Boot application.")
            sys.exit(1)
    except Exception as e:
        print(f"ERROR: Cannot connect to backend server: {str(e)}")
        print("Please ensure the Spring Boot application is running on localhost:8080")
        sys.exit(1)
    
    tester.run_comprehensive_tests()
    
    report_file = f"/home/ubuntu/devin-iris-rahul2/load-testing/reports/performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    tester.generate_report(report_file)
    
    print(f"\nPerformance testing completed!")
    print(f"Report generated: {report_file}")
    
    if tester.results['test_summary']:
        summary = tester.results['test_summary']
        print(f"\nSummary:")
        print(f"- Total tests: {summary['total_tests']}")
        print(f"- Average response time: {summary['overall_avg_response_time']:.2f} ms")
        print(f"- Success rate: {summary['overall_success_rate']:.1f}%")
        print(f"- Fastest response: {summary['fastest_response']:.2f} ms")
        print(f"- Slowest response: {summary['slowest_response']:.2f} ms")

if __name__ == "__main__":
    main()
