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
                dbc.Tab(label="Demographics", tab_id="demographics"),
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
            elif active_tab == "demographics":
                return self.create_demographics_tab(df)
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
    
    def create_demographics_tab(self, df):
        if 'Gender' in df.columns:
            fig1 = px.pie(df, names='Gender', title='Gender Distribution')
        else:
            fig1 = go.Figure()
        
        if 'Level' in df.columns:
            fig2 = px.bar(df['Level'].value_counts(), title='Level Distribution')
        else:
            fig2 = go.Figure()
        
        return dbc.Row([
            dbc.Col([dcc.Graph(figure=fig1)], width=6),
            dbc.Col([dcc.Graph(figure=fig2)], width=6)
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
