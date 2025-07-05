# Bench Analytics Framework

A comprehensive analytics solution for workforce bench capacity management with 152 data fields covering employee demographics, project allocations, skills, training, and performance metrics.

## Overview

This framework analyzes workforce data to provide insights into:
- Employee demographics and distribution
- Project allocation patterns and efficiency
- Skills inventory and training needs
- Bench management and ageing analysis
- Performance metrics and RAG status tracking
- Workforce planning and capacity forecasting

## Data Structure

The framework handles 152 columns organized into 9 categories:

### 1. Employee Information (12 columns)
- Employee Code, Name, Gender, Level, Designation
- Employment Status, Nature of Employment, Date of Joining
- Total Experience, Email ID, Mobile Number, Visa

### 2. Location Information (5 columns)
- Location, Base Location, State, Region, Work Mode

### 3. Project Allocation (12 columns)
- Client Name, Project Name, Project Department, Project Type
- Allocation dates, Loading Percentage, SOW Role, Primary Role

### 4. Skills & Training (12 columns)
- Primary/Secondary technical skills
- Training plans, status, and needs identification
- Certifications and skill update tracking

### 5. Bench Management (9 columns)
- Status, Bench Category, Reason for Bench
- Current/Actual Ageing, Ageing Slabs
- Extended bench reasons and remarks

### 6. Workforce Planning (8 columns)
- BU Owner, WFM Owner, Plan Status and Dates
- Expected allocations and availability flags

### 7. Performance Metrics (7 columns)
- Associate RAG Status, SME Evaluations
- Evaluation tools and scores, ATL eligibility

### 8. HR Administration (8 columns)
- HRBP, BGV Status, Contract details
- Notice Period, Offer Type, LOB

### 9. Separation Information (8 columns)
- Resignation dates, separation nature and reasons
- Last working day, resignation status

## Features

### Data Processing
- **Automated data loading** from Excel files
- **Data validation** and cleaning functions
- **Sample data generation** for testing and demos
- **Category-based column organization**

### Analytics Capabilities
- **Basic workforce statistics** (headcount, allocation rates, bench percentage)
- **Skill distribution analysis** with primary/secondary skill tracking
- **Location-wise workforce distribution**
- **Bench ageing analysis** with configurable time ranges
- **Performance metrics** including RAG status tracking

### Visualizations
- **Employee Demographics**: Gender, level, location, experience distributions
- **Bench Analysis**: Status distribution, category breakdown, ageing patterns
- **Skills Analysis**: Skill inventory, training status, competency mapping
- **Allocation Analysis**: Loading patterns, client distribution, project timelines

### Interactive Dashboard
- **Web-based interface** with multiple analytics tabs
- **Real-time filtering** by status, location, skills, and other dimensions
- **Drill-down capabilities** for detailed analysis
- **Export functionality** for reports and presentations

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the main analysis:
```bash
python main_analysis.py
```

3. Launch the interactive dashboard:
```bash
python dashboard.py
```

## Usage

### Loading Your Data
```python
from data_processor import BenchAnalyticsProcessor

# Load your Excel file
processor = BenchAnalyticsProcessor('your_file.xlsx')
processor.load_data()

# Get basic statistics
stats = processor.get_basic_stats()
print(stats)
```

### Creating Visualizations
```python
from visualizations import BenchAnalyticsVisualizer

visualizer = BenchAnalyticsVisualizer(processor)

# Create demographic analysis
demographics_chart = visualizer.create_employee_demographics_chart('demographics.png')

# Create bench analysis
bench_chart = visualizer.create_bench_analysis_chart('bench_analysis.png')
```

### Running the Dashboard
```python
from dashboard import BenchAnalyticsDashboard

# Launch with your data
dashboard = BenchAnalyticsDashboard('your_file.xlsx')
dashboard.run(port=8050)
```

## Key Metrics Tracked

### Workforce Metrics
- Total headcount and active employees
- Allocation vs bench ratios
- Geographic distribution
- Experience level distribution

### Bench Analytics
- Bench percentage and trends
- Ageing analysis (0-2 weeks, 2-4 weeks, 4-8 weeks, 8+ weeks)
- Category breakdown (Fresh Joiners, Released, Shadow, Training)
- Skill-wise bench distribution

### Performance Indicators
- RAG status distribution (Green, Amber, Red)
- Evaluation scores and feedback
- Training completion rates
- Allocation efficiency metrics

### Skills Intelligence
- Primary and secondary skill inventory
- High-demand vs available skills gap
- Training needs identification
- Certification tracking

## Sample Insights

The framework generates actionable insights such as:
- "15% of workforce is on bench with average ageing of 28 days"
- "Java developers have highest allocation rate at 85%"
- "Bangalore location shows 20% higher bench percentage than average"
- "Fresh joiners represent 40% of current bench population"

## File Structure

```
bench_analytics/
├── data_processor.py      # Core data processing and analysis
├── visualizations.py      # Chart and graph generation
├── dashboard.py          # Interactive web dashboard
├── main_analysis.py      # Main analysis script
├── requirements.txt      # Python dependencies
├── README.md            # This documentation
└── outputs/             # Generated charts and reports
    ├── demographics_analysis.png
    ├── bench_analysis.png
    ├── skills_analysis.png
    ├── allocation_analysis.png
    └── interactive_dashboard.html
```

## Customization

The framework is designed to be easily customizable:

1. **Add new metrics** by extending the `BenchAnalyticsProcessor` class
2. **Create custom visualizations** by adding methods to `BenchAnalyticsVisualizer`
3. **Modify dashboard layout** by updating the `BenchAnalyticsDashboard` class
4. **Adjust column categories** by modifying the `_define_column_categories` method

## Best Practices

1. **Data Quality**: Ensure consistent data formats and handle missing values appropriately
2. **Regular Updates**: Refresh analytics weekly or monthly for trending analysis
3. **Stakeholder Alignment**: Customize metrics based on organizational KPIs
4. **Action-Oriented**: Use insights to drive concrete workforce planning decisions

## Support

For questions or customization requests, refer to the code documentation or extend the existing classes to meet your specific requirements.
