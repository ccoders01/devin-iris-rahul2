import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from data_processor import BenchAnalyticsProcessor
from visualizations import BenchAnalyticsVisualizer

class BenchAnalyticsDashboard:
    def __init__(self, data_file=None):
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.processor = BenchAnalyticsProcessor(data_file)
        
        if data_file:
            self.processor.load_data()
        else:
            self.processor.generate_sample_data()
            
        self.visualizer = BenchAnalyticsVisualizer(self.processor)
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        self.app.layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("Bench Analytics Dashboard", className="text-center mb-4"),
                    html.Hr()
                ])
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Key Metrics", className="card-title"),
                            html.Div(id="key-metrics")
                        ])
                    ])
                ], width=12)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Filters", className="card-title"),
                            dbc.Row([
                                dbc.Col([
                                    html.Label("Status:"),
                                    dcc.Dropdown(
                                        id="status-filter",
                                        options=[{"label": "All", "value": "All"}],
                                        value="All",
                                        multi=True
                                    )
                                ], width=6),
                                dbc.Col([
                                    html.Label("Location:"),
                                    dcc.Dropdown(
                                        id="location-filter",
                                        options=[{"label": "All", "value": "All"}],
                                        value="All",
                                        multi=True
                                    )
                                ], width=6)
                            ])
                        ])
                    ])
                ], width=12)
            ], className="mb-4"),
            
            dbc.Tabs([
                dbc.Tab(label="Overview", tab_id="overview"),
                dbc.Tab(label="Bench Analysis", tab_id="bench"),
                dbc.Tab(label="Skills Analysis", tab_id="skills"),
                dbc.Tab(label="Trends", tab_id="trends"),
                dbc.Tab(label="Data Table", tab_id="data")
            ], id="tabs", active_tab="overview"),
            
            html.Div(id="tab-content", className="mt-4")
        ], fluid=True)
    
    def setup_callbacks(self):
        @self.app.callback(
            [Output("status-filter", "options"),
             Output("location-filter", "options")],
            [Input("tabs", "active_tab")]
        )
        def update_filter_options(active_tab):
            df = self.processor.df
            
            status_options = [{"label": "All", "value": "All"}]
            if 'Status' in df.columns:
                status_options.extend([{"label": status, "value": status} 
                                     for status in df['Status'].unique() if pd.notna(status)])
            
            location_options = [{"label": "All", "value": "All"}]
            if 'Location' in df.columns:
                location_options.extend([{"label": loc, "value": loc} 
                                       for loc in df['Location'].unique() if pd.notna(loc)])
            
            return status_options, location_options
        
        @self.app.callback(
            Output("key-metrics", "children"),
            [Input("status-filter", "value"),
             Input("location-filter", "value")]
        )
        def update_key_metrics(status_filter, location_filter):
            df = self.processor.df.copy()
            
            if status_filter and "All" not in status_filter:
                df = df[df['Status'].isin(status_filter)]
            if location_filter and "All" not in location_filter:
                df = df[df['Location'].isin(location_filter)]
            
            total_employees = len(df)
            bench_count = len(df[df['Status'] == 'Bench']) if 'Status' in df.columns else 0
            allocated_count = len(df[df['Status'] == 'Allocated']) if 'Status' in df.columns else 0
            bench_percentage = (bench_count / total_employees * 100) if total_employees > 0 else 0
            
            return dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3(f"{total_employees}", className="text-primary"),
                            html.P("Total Employees")
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3(f"{allocated_count}", className="text-success"),
                            html.P("Allocated")
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3(f"{bench_count}", className="text-warning"),
                            html.P("On Bench")
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3(f"{bench_percentage:.1f}%", className="text-info"),
                            html.P("Bench %")
                        ])
                    ])
                ], width=3)
            ])
        
        @self.app.callback(
            Output("tab-content", "children"),
            [Input("tabs", "active_tab"),
             Input("status-filter", "value"),
             Input("location-filter", "value")]
        )
        def update_tab_content(active_tab, status_filter, location_filter):
            df = self.processor.df.copy()
            
            if status_filter and "All" not in status_filter:
                df = df[df['Status'].isin(status_filter)]
            if location_filter and "All" not in location_filter:
                df = df[df['Location'].isin(location_filter)]
            
            if active_tab == "overview":
                return self.create_overview_tab(df)
            elif active_tab == "bench":
                return self.create_bench_tab(df)
            elif active_tab == "skills":
                return self.create_skills_tab(df)
            elif active_tab == "trends":
                return self.create_trends_tab(df)
            elif active_tab == "data":
                return self.create_data_tab(df)
            
            return html.Div("Select a tab")
    
    def create_overview_tab(self, df):
        fig1 = px.pie(df, names='Status', title='Employee Status Distribution')
        
        if 'Location' in df.columns:
            location_counts = df['Location'].value_counts().head(10)
            fig2 = px.bar(x=location_counts.index, y=location_counts.values, 
                         title='Top 10 Locations')
        else:
            fig2 = go.Figure()
        
        return dbc.Row([
            dbc.Col([dcc.Graph(figure=fig1)], width=6),
            dbc.Col([dcc.Graph(figure=fig2)], width=6)
        ])
    
    def create_bench_tab(self, df):
        bench_df = df[df['Status'] == 'Bench'] if 'Status' in df.columns else pd.DataFrame()
        
        if len(bench_df) == 0:
            return html.Div("No bench employees found with current filters")
        
        fig1 = px.pie(bench_df, names='Bench Category', title='Bench Category Distribution')
        
        if 'Current Ageing' in bench_df.columns:
            ageing_data = pd.to_numeric(bench_df['Current Ageing'], errors='coerce').dropna()
            fig2 = px.histogram(ageing_data, title='Bench Ageing Distribution', 
                              labels={'value': 'Days on Bench', 'count': 'Frequency'})
        else:
            fig2 = go.Figure()
        
        return dbc.Row([
            dbc.Col([dcc.Graph(figure=fig1)], width=6),
            dbc.Col([dcc.Graph(figure=fig2)], width=6)
        ])
    
    def create_skills_tab(self, df):
        if 'Tech1 Primary Skill' in df.columns:
            skill_counts = df['Tech1 Primary Skill'].value_counts().head(10)
            fig1 = px.bar(x=skill_counts.index, y=skill_counts.values, 
                         title='Top 10 Primary Skills')
        else:
            fig1 = go.Figure()
        
        if 'Associate RAG Status' in df.columns:
            fig2 = px.pie(df, names='Associate RAG Status', title='RAG Status Distribution')
        else:
            fig2 = go.Figure()
        
        return dbc.Row([
            dbc.Col([dcc.Graph(figure=fig1)], width=6),
            dbc.Col([dcc.Graph(figure=fig2)], width=6)
        ])
    
    def create_trends_tab(self, df):
        if 'Actual Ageing Slab' in df.columns:
            slab_counts = df['Actual Ageing Slab'].value_counts()
            
            slab_order = ['0-1 Wks', '1-2 Wks', '2-3 Wks', '3-4 Wks', '4-5 Wks', '5-6 Wks', 
                         '6-7 Wks', '7-8 Wks', '8-9 Wks', '9-10 Wks', '10-11 Wks', '11-12 Wks',
                         '12-13 Wks', '13-14 Wks', '14-15 Wks', '15-16 Wks', '16-18 Wks', 
                         '18-20 Wks', '20-22 Wks', '22-24 Wks', '24-25 Wks', '>25 Wks']
            
            progression_counts = []
            x_labels = []
            
            for slab in slab_order:
                if slab in slab_counts.index:
                    progression_counts.append(slab_counts[slab])
                    x_labels.append(slab)
            
            fig1 = go.Figure(data=[go.Scatter(
                x=x_labels, 
                y=progression_counts,
                mode='lines+markers',
                line=dict(width=3, color='#1f77b4'),
                marker=dict(size=8, color='#1f77b4'),
                fill='tonexty',
                fillcolor='rgba(31, 119, 180, 0.1)'
            )])
            
            fig1.update_layout(
                title="Employee Progression Through Ageing Slabs", 
                height=400,
                xaxis_title="Ageing Slab",
                yaxis_title="Employee Count",
                xaxis=dict(tickangle=45),
                showlegend=False
            )
        else:
            fig1 = go.Figure()
            fig1.update_layout(title='Ageing Trends - Actual Ageing Slab Column Not Found', height=400)
        
        if 'Planned ReleaseDate' in self.processor.df.columns:
            valid_dates = pd.to_datetime(self.processor.df['Planned ReleaseDate'], errors='coerce')
            valid_dates = valid_dates.dropna()
            
            if len(valid_dates) > 0:
                monthly_counts = valid_dates.dt.to_period('M').value_counts().sort_index()
                
                months = [period.strftime('%b %Y') for period in monthly_counts.index]
                counts = monthly_counts.values.tolist()
                
                fig2 = go.Figure(data=[go.Scatter(
                    x=months,
                    y=counts,
                    mode='lines+markers',
                    line=dict(width=3, color='#ff7f0e'),
                    marker=dict(size=8, color='#ff7f0e')
                )])
                
                fig2.update_layout(
                    title="Projected Bench - Monthly Release Projections (All Categories)", 
                    height=400,
                    xaxis_title="Month",
                    yaxis_title="Employee Count",
                    xaxis=dict(tickangle=45),
                    showlegend=False
                )
            else:
                fig2 = go.Figure()
                fig2.update_layout(title="Projected Bench - No Valid Release Dates Found", height=400)
        else:
            fig2 = go.Figure()
            fig2.update_layout(title="Projected Bench - Planned ReleaseDate Column Not Found", height=400)
        
        return dbc.Row([
            dbc.Col([dcc.Graph(figure=fig1)], width=12),
            dbc.Col([dcc.Graph(figure=fig2)], width=12)
        ])
    
    def create_data_tab(self, df):
        return dash_table.DataTable(
            data=df.head(100).to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=20,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
        )
    
    def run(self, debug=True, port=8050):
        self.app.run_server(debug=debug, port=port, host='0.0.0.0')

if __name__ == "__main__":
    dashboard = BenchAnalyticsDashboard()
    dashboard.run()
