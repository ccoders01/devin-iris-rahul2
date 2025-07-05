import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class BenchAnalyticsVisualizer:
    def __init__(self, processor):
        self.processor = processor
        self.df = processor.df
        plt.style.use('default')
        sns.set_palette("husl")
        
    def create_employee_trends_chart(self, save_path=None):
        if self.df is None or len(self.df) == 0:
            return None
            
        fig, ax = plt.subplots(1, 1, figsize=(15, 8))
        fig.suptitle('Cumulative Ageing Trends by Week Slabs', fontsize=16, fontweight='bold')
        
        if 'Actual Ageing Slab' in self.df.columns:
            slab_counts = self.df['Actual Ageing Slab'].value_counts()
            
            slab_order = ['0-1 Wks', '1-2 Wks', '2-3 Wks', '3-4 Wks', '4-5 Wks', '5-6 Wks', 
                         '6-7 Wks', '7-8 Wks', '8-9 Wks', '9-10 Wks', '10-11 Wks', '11-12 Wks',
                         '12-13 Wks', '13-14 Wks', '14-15 Wks', '15-16 Wks', '16-18 Wks', 
                         '18-20 Wks', '20-22 Wks', '22-24 Wks', '24-25 Wks', '>25 Wks']
            
            cumulative_counts = []
            cumulative_total = 0
            x_labels = []
            
            for slab in slab_order:
                if slab in slab_counts.index:
                    cumulative_total += slab_counts[slab]
                    cumulative_counts.append(cumulative_total)
                    x_labels.append(slab)
            
            ax.plot(x_labels, cumulative_counts, marker='o', linewidth=3, markersize=8, color='#1f77b4')
            ax.fill_between(x_labels, cumulative_counts, alpha=0.3, color='#1f77b4')
            ax.set_title('Cumulative Ageing Trends by Week Slabs')
            ax.set_xlabel('Ageing Slab')
            ax.set_ylabel('Cumulative Employee Count')
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, alpha=0.3)
        else:
            ax.text(0.5, 0.5, 'Actual Ageing Slab data not available', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Ageing Trends - No Data Available')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Trends chart saved to: {save_path}")
        
        return fig
    
    def create_bench_analysis_chart(self, save_path=None):
        if self.df is None or len(self.df) == 0:
            return None
            
        bench_df = self.df[self.df['Status'] == 'Bench'] if 'Status' in self.df.columns else pd.DataFrame()
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Bench Analysis Dashboard', fontsize=16, fontweight='bold')
        
        if 'Status' in self.df.columns:
            status_counts = self.df['Status'].value_counts()
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
            axes[0, 0].pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%', 
                          colors=colors[:len(status_counts)], startangle=90)
            axes[0, 0].set_title('Employee Status Distribution')
        
        if len(bench_df) > 0 and 'Bench Category' in bench_df.columns:
            bench_cat_counts = bench_df['Bench Category'].value_counts()
            axes[0, 1].bar(bench_cat_counts.index, bench_cat_counts.values, color='coral')
            axes[0, 1].set_title('Bench Category Distribution')
            axes[0, 1].set_xlabel('Category')
            axes[0, 1].set_ylabel('Count')
            axes[0, 1].tick_params(axis='x', rotation=45)
        
        if len(bench_df) > 0 and 'Current Ageing' in bench_df.columns:
            ageing_data = pd.to_numeric(bench_df['Current Ageing'], errors='coerce').dropna()
            if len(ageing_data) > 0:
                axes[1, 0].hist(ageing_data, bins=15, color='lightcoral', alpha=0.7, edgecolor='black')
                axes[1, 0].set_title('Bench Ageing Distribution')
                axes[1, 0].set_xlabel('Days on Bench')
                axes[1, 0].set_ylabel('Frequency')
                axes[1, 0].axvline(ageing_data.mean(), color='red', linestyle='--', 
                                  label=f'Mean: {ageing_data.mean():.1f} days')
                axes[1, 0].legend()
        
        if len(bench_df) > 0 and 'Tech1 Primary Skill' in bench_df.columns:
            skill_counts = bench_df['Tech1 Primary Skill'].value_counts().head(8)
            axes[1, 1].barh(skill_counts.index, skill_counts.values, color='lightblue')
            axes[1, 1].set_title('Top Skills on Bench')
            axes[1, 1].set_xlabel('Count')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Bench analysis chart saved to: {save_path}")
        
        return fig
    
    def create_skills_analysis_chart(self, save_path=None):
        if self.df is None or len(self.df) == 0:
            return None
            
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Skills & Training Analysis', fontsize=16, fontweight='bold')
        
        if 'Tech1 Primary Skill' in self.df.columns:
            skill_counts = self.df['Tech1 Primary Skill'].value_counts().head(10)
            axes[0, 0].bar(skill_counts.index, skill_counts.values, color='steelblue')
            axes[0, 0].set_title('Top 10 Primary Skills')
            axes[0, 0].set_xlabel('Skills')
            axes[0, 0].set_ylabel('Count')
            axes[0, 0].tick_params(axis='x', rotation=45)
        
        if 'Training Status' in self.df.columns:
            training_counts = self.df['Training Status'].value_counts()
            axes[0, 1].pie(training_counts.values, labels=training_counts.index, autopct='%1.1f%%', startangle=90)
            axes[0, 1].set_title('Training Status Distribution')
        
        if 'Associate RAG Status' in self.df.columns:
            rag_counts = self.df['Associate RAG Status'].value_counts()
            colors = {'Green': 'green', 'Amber': 'orange', 'Red': 'red'}
            bar_colors = [colors.get(status, 'gray') for status in rag_counts.index]
            axes[1, 0].bar(rag_counts.index, rag_counts.values, color=bar_colors)
            axes[1, 0].set_title('Associate RAG Status')
            axes[1, 0].set_xlabel('Status')
            axes[1, 0].set_ylabel('Count')
        
        if 'Level' in self.df.columns and 'Tech1 Primary Skill' in self.df.columns:
            skill_level_crosstab = pd.crosstab(self.df['Level'], self.df['Tech1 Primary Skill'])
            skill_level_crosstab_top = skill_level_crosstab.iloc[:, :5]
            skill_level_crosstab_top.plot(kind='bar', stacked=True, ax=axes[1, 1])
            axes[1, 1].set_title('Skills by Level Distribution')
            axes[1, 1].set_xlabel('Level')
            axes[1, 1].set_ylabel('Count')
            axes[1, 1].legend(title='Skills', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Skills analysis chart saved to: {save_path}")
        
        return fig
    
    def create_allocation_analysis_chart(self, save_path=None):
        if self.df is None or len(self.df) == 0:
            return None
            
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Project Allocation Analysis', fontsize=16, fontweight='bold')
        
        allocated_df = self.df[self.df['Status'] == 'Allocated'] if 'Status' in self.df.columns else pd.DataFrame()
        
        if 'Loading Percentage' in self.df.columns:
            loading_data = pd.to_numeric(self.df['Loading Percentage'], errors='coerce').dropna()
            if len(loading_data) > 0:
                axes[0, 0].hist(loading_data, bins=10, color='lightgreen', alpha=0.7, edgecolor='black')
                axes[0, 0].set_title('Loading Percentage Distribution')
                axes[0, 0].set_xlabel('Loading %')
                axes[0, 0].set_ylabel('Frequency')
        
        if len(allocated_df) > 0 and 'Client Name' in allocated_df.columns:
            client_counts = allocated_df['Client Name'].value_counts().head(8)
            axes[0, 1].barh(client_counts.index, client_counts.values, color='gold')
            axes[0, 1].set_title('Top Clients by Allocation')
            axes[0, 1].set_xlabel('Count')
        
        if 'Status' in self.df.columns and 'Location' in self.df.columns:
            status_location = pd.crosstab(self.df['Location'], self.df['Status'])
            status_location.plot(kind='bar', stacked=True, ax=axes[1, 0])
            axes[1, 0].set_title('Status Distribution by Location')
            axes[1, 0].set_xlabel('Location')
            axes[1, 0].set_ylabel('Count')
            axes[1, 0].legend(title='Status')
            axes[1, 0].tick_params(axis='x', rotation=45)
        
        if 'Level' in self.df.columns and 'Status' in self.df.columns:
            level_status = pd.crosstab(self.df['Level'], self.df['Status'])
            level_status.plot(kind='bar', ax=axes[1, 1])
            axes[1, 1].set_title('Status Distribution by Level')
            axes[1, 1].set_xlabel('Level')
            axes[1, 1].set_ylabel('Count')
            axes[1, 1].legend(title='Status')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Allocation analysis chart saved to: {save_path}")
        
        return fig
    
    def create_interactive_dashboard(self):
        if self.df is None or len(self.df) == 0:
            return None
        
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=('Status Distribution', 'Skills Distribution', 
                          'Location Analysis', 'Experience vs Level',
                          'Bench Ageing', 'RAG Status'),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "histogram"}, {"type": "bar"}]]
        )
        
        if 'Status' in self.df.columns:
            status_counts = self.df['Status'].value_counts()
            fig.add_trace(go.Pie(labels=status_counts.index, values=status_counts.values,
                               name="Status"), row=1, col=1)
        
        if 'Tech1 Primary Skill' in self.df.columns:
            skill_counts = self.df['Tech1 Primary Skill'].value_counts().head(8)
            fig.add_trace(go.Bar(x=skill_counts.index, y=skill_counts.values,
                               name="Skills"), row=1, col=2)
        
        if 'Location' in self.df.columns:
            location_counts = self.df['Location'].value_counts().head(8)
            fig.add_trace(go.Bar(x=location_counts.index, y=location_counts.values,
                               name="Locations"), row=2, col=1)
        
        if 'Total Experience' in self.df.columns and 'Level' in self.df.columns:
            exp_data = pd.to_numeric(self.df['Total Experience'], errors='coerce')
            fig.add_trace(go.Scatter(x=self.df['Level'], y=exp_data,
                                   mode='markers', name="Experience vs Level"), row=2, col=2)
        
        bench_df = self.df[self.df['Status'] == 'Bench'] if 'Status' in self.df.columns else pd.DataFrame()
        if len(bench_df) > 0 and 'Current Ageing' in bench_df.columns:
            ageing_data = pd.to_numeric(bench_df['Current Ageing'], errors='coerce').dropna()
            fig.add_trace(go.Histogram(x=ageing_data, name="Bench Ageing"), row=3, col=1)
        
        if 'Associate RAG Status' in self.df.columns:
            rag_counts = self.df['Associate RAG Status'].value_counts()
            fig.add_trace(go.Bar(x=rag_counts.index, y=rag_counts.values,
                               name="RAG Status"), row=3, col=2)
        
        fig.update_layout(height=1200, showlegend=False, 
                         title_text="Bench Analytics Interactive Dashboard")
        
        return fig
