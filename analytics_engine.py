import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from column_mapping import COLUMN_CATEGORIES

class AdvancedAnalyticsEngine:
    def __init__(self, df):
        self.df = df
        self.insights = []
        
    def generate_comprehensive_insights(self):
        insights = {
            'workforce_overview': self._analyze_workforce_overview(),
            'bench_analytics': self._analyze_bench_metrics(),
            'skills_intelligence': self._analyze_skills_landscape(),
            'performance_insights': self._analyze_performance_metrics(),
            'location_analytics': self._analyze_location_distribution(),
            'allocation_efficiency': self._analyze_allocation_patterns(),
            'risk_indicators': self._identify_risk_indicators(),
            'recommendations': self._generate_recommendations()
        }
        return insights
    
    def _analyze_workforce_overview(self):
        total_employees = len(self.df)
        active_employees = len(self.df[self.df['Employment Status'] == 'Active']) if 'Employment Status' in self.df.columns else total_employees
        
        overview = {
            'total_workforce': total_employees,
            'active_employees': active_employees,
            'workforce_utilization': (active_employees / total_employees * 100) if total_employees > 0 else 0
        }
        
        if 'Status' in self.df.columns:
            status_dist = self.df['Status'].value_counts(normalize=True) * 100
            overview['status_breakdown'] = status_dist.to_dict()
            
            allocated_pct = status_dist.get('Allocated', 0)
            bench_pct = status_dist.get('Bench', 0)
            overview['allocation_rate'] = allocated_pct
            overview['bench_rate'] = bench_pct
        
        if 'Gender' in self.df.columns:
            gender_dist = self.df['Gender'].value_counts(normalize=True) * 100
            overview['gender_diversity'] = gender_dist.to_dict()
        
        if 'Total Experience' in self.df.columns:
            exp_data = pd.to_numeric(self.df['Total Experience'], errors='coerce').dropna()
            overview['avg_experience'] = exp_data.mean()
            overview['experience_range'] = {
                'min': exp_data.min(),
                'max': exp_data.max(),
                'median': exp_data.median()
            }
        
        return overview
    
    def _analyze_bench_metrics(self):
        if 'Status' not in self.df.columns:
            return {'message': 'Status column not available for bench analysis'}
        
        bench_df = self.df[self.df['Status'] == 'Bench']
        total_bench = len(bench_df)
        
        if total_bench == 0:
            return {'message': 'No employees currently on bench'}
        
        metrics = {
            'total_bench_count': total_bench,
            'bench_percentage': (total_bench / len(self.df) * 100)
        }
        
        if 'Current Ageing' in bench_df.columns:
            ageing_data = pd.to_numeric(bench_df['Current Ageing'], errors='coerce').dropna()
            metrics['average_ageing_days'] = ageing_data.mean()
            metrics['median_ageing_days'] = ageing_data.median()
            
            metrics['ageing_distribution'] = {
                '0-14_days': len(ageing_data[ageing_data <= 14]),
                '15-30_days': len(ageing_data[(ageing_data > 14) & (ageing_data <= 30)]),
                '31-60_days': len(ageing_data[(ageing_data > 30) & (ageing_data <= 60)]),
                '60+_days': len(ageing_data[ageing_data > 60])
            }
            
            metrics['critical_ageing'] = len(ageing_data[ageing_data > 56])
        
        if 'Bench Category' in bench_df.columns:
            category_dist = bench_df['Bench Category'].value_counts()
            metrics['category_breakdown'] = category_dist.to_dict()
        
        if 'Reason For Bench' in bench_df.columns:
            reason_dist = bench_df['Reason For Bench'].value_counts()
            metrics['bench_reasons'] = reason_dist.to_dict()
        
        return metrics
    
    def _analyze_skills_landscape(self):
        skills_analysis = {}
        
        if 'Tech1 Primary Skill' in self.df.columns:
            primary_skills = self.df['Tech1 Primary Skill'].value_counts()
            skills_analysis['primary_skills_distribution'] = primary_skills.to_dict()
            skills_analysis['top_skills'] = primary_skills.head(10).to_dict()
            skills_analysis['skill_diversity'] = len(primary_skills)
        
        if 'Status' in self.df.columns and 'Tech1 Primary Skill' in self.df.columns:
            bench_skills = self.df[self.df['Status'] == 'Bench']['Tech1 Primary Skill'].value_counts()
            allocated_skills = self.df[self.df['Status'] == 'Allocated']['Tech1 Primary Skill'].value_counts()
            
            skills_analysis['bench_skills'] = bench_skills.to_dict()
            skills_analysis['allocated_skills'] = allocated_skills.to_dict()
            
            skill_allocation_rate = {}
            for skill in primary_skills.index:
                total_skill = primary_skills[skill]
                allocated_skill = allocated_skills.get(skill, 0)
                skill_allocation_rate[skill] = (allocated_skill / total_skill * 100) if total_skill > 0 else 0
            
            skills_analysis['skill_allocation_rates'] = skill_allocation_rate
        
        if 'Training Status' in self.df.columns:
            training_dist = self.df['Training Status'].value_counts()
            skills_analysis['training_status'] = training_dist.to_dict()
        
        return skills_analysis
    
    def _analyze_performance_metrics(self):
        performance = {}
        
        if 'Associate RAG Status' in self.df.columns:
            rag_dist = self.df['Associate RAG Status'].value_counts(normalize=True) * 100
            performance['rag_distribution'] = rag_dist.to_dict()
            
            green_pct = rag_dist.get('Green', 0)
            amber_pct = rag_dist.get('Amber', 0)
            red_pct = rag_dist.get('Red', 0)
            
            performance['performance_health'] = {
                'healthy': green_pct,
                'at_risk': amber_pct,
                'critical': red_pct
            }
        
        if 'SME Evaluation' in self.df.columns:
            eval_dist = self.df['SME Evaluation'].value_counts()
            performance['evaluation_distribution'] = eval_dist.to_dict()
        
        if 'ATL Eligible' in self.df.columns:
            atl_dist = self.df['ATL Eligible'].value_counts()
            performance['atl_eligibility'] = atl_dist.to_dict()
        
        return performance
    
    def _analyze_location_distribution(self):
        location_analysis = {}
        
        if 'Location' in self.df.columns:
            location_dist = self.df['Location'].value_counts()
            location_analysis['location_distribution'] = location_dist.to_dict()
            location_analysis['total_locations'] = len(location_dist)
            
            if 'Status' in self.df.columns:
                location_status = pd.crosstab(self.df['Location'], self.df['Status'], normalize='index') * 100
                location_analysis['location_status_breakdown'] = location_status.to_dict()
                
                location_bench_rates = {}
                for location in location_dist.index:
                    location_df = self.df[self.df['Location'] == location]
                    bench_count = len(location_df[location_df['Status'] == 'Bench'])
                    total_count = len(location_df)
                    location_bench_rates[location] = (bench_count / total_count * 100) if total_count > 0 else 0
                
                location_analysis['location_bench_rates'] = location_bench_rates
        
        if 'Work Mode' in self.df.columns:
            work_mode_dist = self.df['Work Mode'].value_counts(normalize=True) * 100
            location_analysis['work_mode_distribution'] = work_mode_dist.to_dict()
        
        return location_analysis
    
    def _analyze_allocation_patterns(self):
        allocation_analysis = {}
        
        if 'Loading Percentage' in self.df.columns:
            loading_data = pd.to_numeric(self.df['Loading Percentage'], errors='coerce').dropna()
            allocation_analysis['average_loading'] = loading_data.mean()
            allocation_analysis['loading_distribution'] = {
                'under_50': len(loading_data[loading_data < 50]),
                '50_75': len(loading_data[(loading_data >= 50) & (loading_data < 75)]),
                '75_100': len(loading_data[(loading_data >= 75) & (loading_data <= 100)]),
                'over_100': len(loading_data[loading_data > 100])
            }
        
        if 'Client Name' in self.df.columns:
            client_dist = self.df['Client Name'].value_counts()
            allocation_analysis['client_distribution'] = client_dist.head(10).to_dict()
            allocation_analysis['client_concentration'] = {
                'top_3_clients_share': (client_dist.head(3).sum() / client_dist.sum() * 100) if len(client_dist) > 0 else 0
            }
        
        if 'Project Type' in self.df.columns:
            project_type_dist = self.df['Project Type'].value_counts()
            allocation_analysis['project_type_distribution'] = project_type_dist.to_dict()
        
        return allocation_analysis
    
    def _identify_risk_indicators(self):
        risks = []
        
        if 'Status' in self.df.columns:
            bench_pct = len(self.df[self.df['Status'] == 'Bench']) / len(self.df) * 100
            if bench_pct > 20:
                risks.append({
                    'type': 'High Bench Percentage',
                    'severity': 'High',
                    'value': f'{bench_pct:.1f}%',
                    'description': 'Bench percentage exceeds 20% threshold'
                })
        
        if 'Current Ageing' in self.df.columns:
            bench_df = self.df[self.df['Status'] == 'Bench'] if 'Status' in self.df.columns else self.df
            if len(bench_df) > 0:
                ageing_data = pd.to_numeric(bench_df['Current Ageing'], errors='coerce').dropna()
                long_bench = len(ageing_data[ageing_data > 56])
                if long_bench > 0:
                    risks.append({
                        'type': 'Extended Bench Ageing',
                        'severity': 'Medium',
                        'value': f'{long_bench} employees',
                        'description': 'Employees on bench for more than 8 weeks'
                    })
        
        if 'Associate RAG Status' in self.df.columns:
            red_count = len(self.df[self.df['Associate RAG Status'] == 'Red'])
            red_pct = red_count / len(self.df) * 100
            if red_pct > 10:
                risks.append({
                    'type': 'High Red RAG Status',
                    'severity': 'High',
                    'value': f'{red_pct:.1f}%',
                    'description': 'High percentage of employees with Red RAG status'
                })
        
        return risks
    
    def _generate_recommendations(self):
        recommendations = []
        
        if 'Status' in self.df.columns:
            bench_pct = len(self.df[self.df['Status'] == 'Bench']) / len(self.df) * 100
            if bench_pct > 15:
                recommendations.append({
                    'category': 'Bench Management',
                    'priority': 'High',
                    'action': 'Implement aggressive allocation strategy',
                    'description': f'Current bench rate of {bench_pct:.1f}% requires immediate attention'
                })
        
        if 'Tech1 Primary Skill' in self.df.columns and 'Status' in self.df.columns:
            skill_allocation = {}
            for skill in self.df['Tech1 Primary Skill'].unique():
                if pd.notna(skill):
                    skill_df = self.df[self.df['Tech1 Primary Skill'] == skill]
                    allocated = len(skill_df[skill_df['Status'] == 'Allocated'])
                    total = len(skill_df)
                    skill_allocation[skill] = (allocated / total * 100) if total > 0 else 0
            
            low_allocation_skills = [skill for skill, rate in skill_allocation.items() if rate < 70]
            if low_allocation_skills:
                recommendations.append({
                    'category': 'Skills Management',
                    'priority': 'Medium',
                    'action': 'Focus on high-demand skills training',
                    'description': f'Skills with low allocation rates: {", ".join(low_allocation_skills[:3])}'
                })
        
        if 'Current Ageing' in self.df.columns:
            bench_df = self.df[self.df['Status'] == 'Bench'] if 'Status' in self.df.columns else self.df
            if len(bench_df) > 0:
                ageing_data = pd.to_numeric(bench_df['Current Ageing'], errors='coerce').dropna()
                avg_ageing = ageing_data.mean()
                if avg_ageing > 30:
                    recommendations.append({
                        'category': 'Process Improvement',
                        'priority': 'Medium',
                        'action': 'Reduce allocation cycle time',
                        'description': f'Average bench ageing of {avg_ageing:.1f} days exceeds target'
                    })
        
        recommendations.append({
            'category': 'Analytics',
            'priority': 'Low',
            'action': 'Implement regular reporting cadence',
            'description': 'Schedule weekly bench reviews and monthly trend analysis'
        })
        
        return recommendations
