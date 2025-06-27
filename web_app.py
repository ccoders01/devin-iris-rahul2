import dash
from dash import dcc, html, Input, Output, State, callback_context, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import base64
import io
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from data_processor import BenchAnalyticsProcessor
from analytics_engine import AdvancedAnalyticsEngine
from column_mapping import COLUMN_CATEGORIES

class BenchAnalyticsWebApp:
    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.processor = None
        self.analytics_engine = None
        self.current_data = None
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        self.app.layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("🎯 Bench Analytics Dashboard", className="text-center mb-4"),
                    html.P("Upload your Excel file to analyze workforce bench capacity data", 
                           className="text-center text-muted mb-4")
                ])
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("📁 File Upload", className="card-title"),
                            dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Excel File')
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
                                multiple=False
                            ),
                            html.Div(id='upload-status', className="mt-3"),
                            dbc.Button("Generate Sample Data", id="sample-data-btn", 
                                     color="secondary", className="mt-3", size="sm")
                        ])
                    ])
                ], width=12)
            ], className="mb-4"),
            
            html.Div(id='main-content'),
            
            dcc.Store(id='data-store'),
            dcc.Store(id='analytics-store')
        ], fluid=True)
    
    def setup_callbacks(self):
        @self.app.callback(
            [Output('upload-status', 'children'),
             Output('data-store', 'data'),
             Output('main-content', 'children')],
            [Input('upload-data', 'contents'),
             Input('sample-data-btn', 'n_clicks')],
            [State('upload-data', 'filename')]
        )
        def handle_file_upload(contents, sample_clicks, filename):
            ctx = callback_context
            
            if not ctx.triggered:
                return "", None, self.create_welcome_content()
            
            trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
            
            try:
                if trigger_id == 'sample-data-btn' and sample_clicks:
                    processor = BenchAnalyticsProcessor()
                    df = processor.generate_sample_data(500)
                    self.processor = processor
                    self.current_data = df
                    
                    status = dbc.Alert([
                        html.I(className="fas fa-check-circle me-2"),
                        "Sample data generated successfully! (500 employees)"
                    ], color="success")
                    
                    return status, df.to_dict('records'), self.create_dashboard_content()
                
                elif trigger_id == 'upload-data' and contents:
                    content_type, content_string = contents.split(',')
                    decoded = base64.b64decode(content_string)
                    
                    if filename.endswith('.xlsx') or filename.endswith('.xls'):
                        df = pd.read_excel(io.BytesIO(decoded))
                        
                        if len(df) == 0:
                            processor = BenchAnalyticsProcessor()
                            df = processor.generate_sample_data(500)
                            status = dbc.Alert([
                                html.I(className="fas fa-info-circle me-2"),
                                f"File '{filename}' contains only headers. Generated sample data for demonstration."
                            ], color="info")
                        else:
                            processor = BenchAnalyticsProcessor()
                            processor.df = df
                            status = dbc.Alert([
                                html.I(className="fas fa-check-circle me-2"),
                                f"File '{filename}' uploaded successfully! ({len(df)} rows, {len(df.columns)} columns)"
                            ], color="success")
                        
                        self.processor = processor
                        self.current_data = df
                        
                        return status, df.to_dict('records'), self.create_dashboard_content()
                    else:
                        status = dbc.Alert([
                            html.I(className="fas fa-exclamation-triangle me-2"),
                            "Please upload an Excel file (.xlsx or .xls)"
                        ], color="warning")
                        return status, None, self.create_welcome_content()
                        
            except Exception as e:
                status = dbc.Alert([
                    html.I(className="fas fa-times-circle me-2"),
                    f"Error processing file: {str(e)}"
                ], color="danger")
                return status, None, self.create_welcome_content()
            
            return "", None, self.create_welcome_content()
    
    def create_welcome_content(self):
        return dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3("Welcome to Bench Analytics", className="text-center"),
                        html.P("This application analyzes workforce bench capacity data with 152 columns covering:", 
                               className="text-center"),
                        html.Ul([
                            html.Li("Employee Demographics & Information"),
                            html.Li("Project Allocation & Loading"),
                            html.Li("Skills & Training Analysis"),
                            html.Li("Bench Management & Ageing"),
                            html.Li("Performance Metrics & RAG Status"),
                            html.Li("Location & Workforce Distribution")
                        ], className="text-start"),
                        html.Hr(),
                        html.P("Upload your Excel file or generate sample data to get started!", 
                               className="text-center text-muted")
                    ])
                ])
            ], width=8, offset=2)
        ])
    
    def create_dashboard_content(self):
        if not self.processor or self.current_data is None:
            return self.create_welcome_content()
        
        stats = self.processor.get_basic_stats()
        
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("📊 Key Metrics", className="card-title"),
                            dbc.Row([
                                dbc.Col([
                                    html.H3(f"{stats['total_employees']}", className="text-primary"),
                                    html.P("Total Employees", className="text-muted")
                                ], width=3),
                                dbc.Col([
                                    html.H3(f"{stats['bench_percentage']}%", className="text-warning"),
                                    html.P("Bench Rate", className="text-muted")
                                ], width=3),
                                dbc.Col([
                                    html.H3(f"{stats['allocated_count']}", className="text-success"),
                                    html.P("Allocated", className="text-muted")
                                ], width=3),
                                dbc.Col([
                                    html.H3(f"{stats['avg_experience']:.1f}", className="text-info"),
                                    html.P("Avg Experience", className="text-muted")
                                ], width=3)
                            ])
                        ])
                    ])
                ], width=12)
            ], className="mb-4"),
            
            dbc.Tabs([
                dbc.Tab(label="📈 Overview", tab_id="overview"),
                dbc.Tab(label="👥 Demographics", tab_id="demographics"),
                dbc.Tab(label="🏢 Bench Analysis", tab_id="bench"),
                dbc.Tab(label="🎯 Skills", tab_id="skills"),
                dbc.Tab(label="📍 Locations", tab_id="locations"),
                dbc.Tab(label="📋 Data Table", tab_id="data")
            ], id="tabs", active_tab="overview"),
            
            html.Div(id="tab-content", className="mt-4")
        ])
    
    def create_overview_tab(self):
        if not self.processor or self.current_data is None:
            return html.Div("No data available")
        
        df = self.current_data
        
        status_counts = df['Status'].value_counts()
        fig_status = px.pie(values=status_counts.values, names=status_counts.index,
                           title="Employee Status Distribution")
        
        location_counts = df['Location'].value_counts().head(10)
        fig_location = px.bar(x=location_counts.index, y=location_counts.values,
                             title="Top 10 Locations")
        
        return dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_status)
            ], width=6),
            dbc.Col([
                dcc.Graph(figure=fig_location)
            ], width=6)
        ])
    
    def create_demographics_tab(self):
        if not self.processor or self.current_data is None:
            return html.Div("No data available")
        
        df = self.current_data
        
        gender_counts = df['Gender'].value_counts()
        fig_gender = px.pie(values=gender_counts.values, names=gender_counts.index,
                           title="Gender Distribution")
        
        level_counts = df['Level'].value_counts()
        fig_level = px.bar(x=level_counts.index, y=level_counts.values,
                          title="Employee Level Distribution")
        
        fig_experience = px.histogram(df, x='Total Experience', nbins=20,
                                     title="Experience Distribution")
        
        return dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_gender)
            ], width=6),
            dbc.Col([
                dcc.Graph(figure=fig_level)
            ], width=6),
            dbc.Col([
                dcc.Graph(figure=fig_experience)
            ], width=12)
        ])
    
    def create_bench_tab(self):
        if not self.processor or self.current_data is None:
            return html.Div("No data available")
        
        df = self.current_data
        bench_df = df[df['Status'] == 'Bench']
        
        if len(bench_df) == 0:
            return dbc.Alert("No bench employees found in the data", color="info")
        
        category_counts = bench_df['Bench Category'].value_counts()
        fig_category = px.bar(x=category_counts.index, y=category_counts.values,
                             title="Bench Category Distribution")
        
        fig_ageing = px.histogram(bench_df, x='Current Ageing', nbins=20,
                                 title="Bench Ageing Distribution (Days)")
        
        bench_skills = bench_df['Tech1 Primary Skill'].value_counts().head(10)
        fig_skills = px.bar(x=bench_skills.values, y=bench_skills.index,
                           orientation='h', title="Top Skills on Bench")
        
        return dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_category)
            ], width=6),
            dbc.Col([
                dcc.Graph(figure=fig_ageing)
            ], width=6),
            dbc.Col([
                dcc.Graph(figure=fig_skills)
            ], width=12)
        ])
    
    def create_skills_tab(self):
        if not self.processor or self.current_data is None:
            return html.Div("No data available")
        
        df = self.current_data
        
        skill_counts = df['Tech1 Primary Skill'].value_counts().head(15)
        fig_skills = px.bar(x=skill_counts.index, y=skill_counts.values,
                           title="Top 15 Primary Skills")
        
        rag_counts = df['Associate RAG Status'].value_counts()
        fig_rag = px.pie(values=rag_counts.values, names=rag_counts.index,
                        title="RAG Status Distribution",
                        color_discrete_map={'Green': 'green', 'Amber': 'orange', 'Red': 'red'})
        
        return dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_skills)
            ], width=8),
            dbc.Col([
                dcc.Graph(figure=fig_rag)
            ], width=4)
        ])
    
    def create_locations_tab(self):
        if not self.processor or self.current_data is None:
            return html.Div("No data available")
        
        df = self.current_data
        
        location_status = pd.crosstab(df['Location'], df['Status'])
        fig_location_status = px.bar(location_status, title="Status Distribution by Location")
        
        return dbc.Row([
            dbc.Col([
                dcc.Graph(figure=fig_location_status)
            ], width=12)
        ])
    
    def create_data_tab(self):
        if not self.processor or self.current_data is None:
            return html.Div("No data available")
        
        df = self.current_data
        
        display_columns = ['Employee Code', 'Employee Name', 'Gender', 'Level', 
                          'Location', 'Status', 'Tech1 Primary Skill', 'Total Experience']
        
        available_columns = [col for col in display_columns if col in df.columns]
        if not available_columns:
            return html.Div("No displayable columns found in data")
            
        display_df = df[available_columns].head(100)
        
        return html.Div([
            html.H4("Data Preview (First 100 rows)"),
            dash_table.DataTable(
                data=display_df.to_dict('records'),
                columns=[{"name": i, "id": i} for i in available_columns],
                page_size=20,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '10px'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
            )
        ])
    
    def setup_tab_callback(self):
        @self.app.callback(
            Output("tab-content", "children"),
            Input("tabs", "active_tab")
        )
        def render_tab_content(active_tab):
            if active_tab == "overview":
                return self.create_overview_tab()
            elif active_tab == "demographics":
                return self.create_demographics_tab()
            elif active_tab == "bench":
                return self.create_bench_tab()
            elif active_tab == "skills":
                return self.create_skills_tab()
            elif active_tab == "locations":
                return self.create_locations_tab()
            elif active_tab == "data":
                return self.create_data_tab()
            return html.Div("Select a tab to view content")
    
    def run(self, host='0.0.0.0', port=8050, debug=False):
        self.setup_tab_callback()
        print(f"🚀 Starting Bench Analytics Web Application...")
        print(f"📱 Access the dashboard at: http://localhost:{port}")
        self.app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    app = BenchAnalyticsWebApp()
    app.run(debug=True)
