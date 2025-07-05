import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class BenchAnalyticsProcessor:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.df = None
        self.column_categories = self._define_column_categories()
        
    def _define_column_categories(self):
        return {
            'employee_info': [
                'Employee Code', 'Employee Name', 'Gender', 'Level', 'Designation',
                'Employment Status', 'Nature Of Employment', 'Date of Joining',
                'Total Experience', 'Email ID', 'Mobile Number', 'Visa'
            ],
            'location_info': [
                'Location', 'Base Location', 'State', 'Region', 'Work Mode'
            ],
            'project_allocation': [
                'Client Name', 'Project Name', 'Project Department', 'Project Type',
                'Actual Allocation Start Date', 'Expected Billing Start Date',
                'Allocation Start Date', 'Allocation End Date', 'Loading Percentage',
                'Planned ReleaseDate', 'SOW Role', 'Primary Ro'
            ],
            'skills_training': [
                'Tech1 Primary Skill', 'Tech1 NonPrimary Skill', 'Tech2 Primary Skill',
                'Tech2 NonPrimary Skill', 'Training Plan', 'Training Need Identified',
                'Tech1 For Training', 'Tech 2 For Training', 'Training Status',
                'Certifications', 'Skill', 'Last Skill Update on'
            ],
            'bench_management': [
                'Status', 'Bench Category', 'Reason For Bench', 'Current Ageing',
                'Actual Ageing', 'Current Ageing Slab', 'Actual Ageing Slab',
                'Bench Ageing >8Wks Reason', 'Bench Ageing >8Wks Remarks'
            ],
            'workforce_planning': [
                'BU Owner', 'WFM Owner Name', 'WFM Plan Status', 'WFM Plan Date',
                'Expected Allocation Start Date', 'Expected Client Name',
                'Expected Project Name', 'Available for Other BU'
            ],
            'performance_metrics': [
                'Associate RAG Status', 'SME Evaluation', 'Evaluation Tool',
                'No Of Evaluation', 'Last Evaluation Reason', 'ATL Eligible',
                'Associate Classification', 'Potential ATL'
            ],
            'hr_admin': [
                'HRBP', 'BGV Status', 'BGV Closure Status', 'Expected BGV Closure Date',
                'Contract EndDate', 'Notice Period', 'Offer Type', 'LOB'
            ],
            'separation_info': [
                'Date Of Resignation', 'Last Working Day', 'Nature Of Separation',
                'Reason', 'Primary Reason', 'Resignation Status', 'Last Release Reason'
            ]
        }
    
    def load_data(self, file_path=None):
        if file_path:
            self.file_path = file_path
        
        if not self.file_path:
            raise ValueError("No file path provided")
            
        try:
            self.df = pd.read_excel(self.file_path)
            print(f"Data loaded successfully: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def generate_sample_data(self, num_rows=500):
        np.random.seed(42)
        
        sample_data = {}
        
        sample_data['Employee Code'] = [f'EMP{str(i).zfill(5)}' for i in range(1, num_rows + 1)]
        sample_data['Employee Name'] = [f'Employee {i}' for i in range(1, num_rows + 1)]
        sample_data['Gender'] = np.random.choice(['Male', 'Female'], num_rows, p=[0.6, 0.4])
        sample_data['Level'] = np.random.choice(['L1', 'L2', 'L3', 'L4', 'L5'], num_rows, p=[0.3, 0.25, 0.2, 0.15, 0.1])
        sample_data['Designation'] = np.random.choice([
            'Software Engineer', 'Senior Software Engineer', 'Tech Lead', 
            'Architect', 'Manager', 'Senior Manager', 'Consultant', 'Senior Consultant'
        ], num_rows)
        
        sample_data['Employment Status'] = np.random.choice(['Active', 'Inactive'], num_rows, p=[0.9, 0.1])
        sample_data['Location'] = np.random.choice([
            'Bangalore', 'Hyderabad', 'Chennai', 'Mumbai', 'Pune', 'Delhi', 'Kolkata'
        ], num_rows)
        
        sample_data['Status'] = np.random.choice([
            'Allocated', 'Bench', 'Training', 'Notice Period', 'On Leave'
        ], num_rows, p=[0.7, 0.15, 0.08, 0.05, 0.02])
        
        bench_mask = np.array(sample_data['Status']) == 'Bench'
        bench_categories = np.random.choice(['Fresh Joiners', 'Released', 'Shadow', 'Training'], 
                                          sum(bench_mask))
        sample_data['Bench Category'] = [''] * num_rows
        bench_idx = 0
        for i in range(num_rows):
            if bench_mask[i]:
                sample_data['Bench Category'][i] = bench_categories[bench_idx]
                bench_idx += 1
        
        bench_mask = np.array(sample_data['Status']) == 'Bench'
        bench_ageing = np.random.randint(1, 120, sum(bench_mask))
        sample_data['Current Ageing'] = [0] * num_rows
        bench_idx = 0
        for i in range(num_rows):
            if bench_mask[i]:
                sample_data['Current Ageing'][i] = bench_ageing[bench_idx]
                bench_idx += 1
        
        sample_data['Tech1 Primary Skill'] = np.random.choice([
            'Java', 'Python', '.NET', 'React', 'Angular', 'Node.js', 'AWS', 'Azure'
        ], num_rows)
        
        sample_data['Total Experience'] = np.random.uniform(0.5, 15, num_rows).round(1)
        
        allocated_mask = np.array(sample_data['Status']) == 'Allocated'
        allocated_loading = np.random.choice([50, 75, 100], sum(allocated_mask))
        sample_data['Loading Percentage'] = [0] * num_rows
        allocated_idx = 0
        for i in range(num_rows):
            if allocated_mask[i]:
                sample_data['Loading Percentage'][i] = allocated_loading[allocated_idx]
                allocated_idx += 1
        
        sample_data['Associate RAG Status'] = np.random.choice([
            'Green', 'Amber', 'Red'
        ], num_rows, p=[0.7, 0.2, 0.1])
        
        sample_data['ATL Eligible'] = np.random.choice([
            'Yes', 'No', 'Under Review'
        ], num_rows, p=[0.3, 0.6, 0.1])
        
        sample_data['Resignation Status'] = np.random.choice([
            '', 'Submitted', 'Approved', 'Withdrawn'
        ], num_rows, p=[0.85, 0.08, 0.05, 0.02])
        
        sample_data['Potential ATL'] = np.random.choice([
            'High', 'Medium', 'Low', ''
        ], num_rows, p=[0.15, 0.25, 0.35, 0.25])
        
        start_date = pd.Timestamp.now() - pd.DateOffset(years=5)
        end_date = pd.Timestamp.now()
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        sample_data['Date of Joining'] = np.random.choice(date_range, size=num_rows)
        
        clients = ['Acme Corp', 'TechFlow Inc', 'DataSys Ltd', 'CloudTech', 'InnovateCo', 
                  'GlobalSoft', 'NextGen Solutions', 'DigitalEdge', 'SmartSystems', 'FutureTech']
        projects = ['Digital Transformation', 'Cloud Migration', 'Data Analytics Platform', 
                   'Mobile App Development', 'AI/ML Platform', 'E-commerce Portal', 
                   'CRM System', 'ERP Implementation', 'DevOps Automation', 'Cybersecurity Enhancement']
        
        sample_data['Client Name'] = ['' for _ in range(num_rows)]
        sample_data['Project Name'] = ['' for _ in range(num_rows)]
        
        allocated_mask = np.array(sample_data['Status']) == 'Allocated'
        if allocated_mask.sum() > 0:
            sample_data['Client Name'] = [
                np.random.choice(clients) if allocated_mask[i] else ''
                for i in range(num_rows)
            ]
            sample_data['Project Name'] = [
                np.random.choice(projects) if allocated_mask[i] else ''
                for i in range(num_rows)
            ]
        
        allocated_mask = np.array(sample_data['Status']) == 'Allocated'
        if allocated_mask.sum() > 0:
            start_date = pd.Timestamp.now() + pd.DateOffset(months=1)
            end_date = pd.Timestamp.now() + pd.DateOffset(months=12)
            future_dates = pd.date_range(start=start_date, end=end_date, freq='D')
            
            sample_data['Planned ReleaseDate'] = ['' for _ in range(num_rows)]
            for i in range(num_rows):
                if allocated_mask[i]:
                    sample_data['Planned ReleaseDate'][i] = np.random.choice(future_dates)
        
        for col in self.column_categories['employee_info'] + \
                   self.column_categories['location_info'] + \
                   self.column_categories['project_allocation'] + \
                   self.column_categories['skills_training'] + \
                   self.column_categories['bench_management'] + \
                   self.column_categories['workforce_planning'] + \
                   self.column_categories['performance_metrics'] + \
                   self.column_categories['hr_admin'] + \
                   self.column_categories['separation_info']:
            if col not in sample_data:
                sample_data[col] = ['' for _ in range(num_rows)]
        
        self.df = pd.DataFrame(sample_data)
        print(f"Sample data generated: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        return self.df
    
    def get_basic_stats(self):
        if self.df is None:
            return "No data loaded"
        
        stats = {
            'total_employees': len(self.df),
            'active_employees': len(self.df[self.df['Employment Status'] == 'Active']),
            'bench_count': len(self.df[self.df['Status'] == 'Bench']),
            'allocated_count': len(self.df[self.df['Status'] == 'Allocated']),
            'bench_percentage': round(len(self.df[self.df['Status'] == 'Bench']) / len(self.df) * 100, 2),
            'avg_experience': self.df['Total Experience'].mean() if 'Total Experience' in self.df.columns else 0
        }
        return stats
    
    def get_skill_distribution(self):
        if self.df is None or 'Tech1 Primary Skill' not in self.df.columns:
            return {}
        
        return self.df['Tech1 Primary Skill'].value_counts().to_dict()
    
    def get_location_distribution(self):
        if self.df is None or 'Location' not in self.df.columns:
            return {}
        
        return self.df['Location'].value_counts().to_dict()
    
    def get_bench_analysis(self):
        if self.df is None:
            return {}
        
        bench_df = self.df[self.df['Status'] == 'Bench']
        if len(bench_df) == 0:
            return {'message': 'No bench employees found'}
        
        analysis = {
            'total_bench': len(bench_df),
            'avg_ageing': bench_df['Current Ageing'].mean() if 'Current Ageing' in bench_df.columns else 0,
            'category_distribution': bench_df['Bench Category'].value_counts().to_dict() if 'Bench Category' in bench_df.columns else {},
            'ageing_ranges': {
                '0-2 weeks': len(bench_df[bench_df['Current Ageing'] <= 14]),
                '2-4 weeks': len(bench_df[(bench_df['Current Ageing'] > 14) & (bench_df['Current Ageing'] <= 28)]),
                '4-8 weeks': len(bench_df[(bench_df['Current Ageing'] > 28) & (bench_df['Current Ageing'] <= 56)]),
                '8+ weeks': len(bench_df[bench_df['Current Ageing'] > 56])
            } if 'Current Ageing' in bench_df.columns else {}
        }
        return analysis
