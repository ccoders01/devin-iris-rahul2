#!/usr/bin/env python3
"""
Simple Flask Web Application for Bench Analytics
A more reliable alternative to the Dash implementation
"""

from flask import Flask, render_template, request, jsonify, send_file, Response
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.utils
import json
import io
import base64
from data_processor import BenchAnalyticsProcessor

def filter_by_categories(df, selected_categories):
    """Filter dataframe by selected categories. If no categories selected, return all data."""
    if not selected_categories or len(selected_categories) == 0:
        return df
    
    filtered_df = df[df['Status'].isin(selected_categories)]
    
    if len(filtered_df) == 0:
        return df
    
    return filtered_df

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

EXCEL_FILE_PATH = '/home/ubuntu/attachments/12b1bb37-764b-4db6-8704-1c4922cc604a/Original_Bench+capacity+Jun+24.xlsx'
processor = None
current_data = None

def initialize_data():
    global processor, current_data
    try:
        processor = BenchAnalyticsProcessor(EXCEL_FILE_PATH)
        if processor.load_data():
            current_data = processor.df
            stats = processor.get_basic_stats()
            print(f"✅ Real data loaded successfully: {stats['total_employees']} employees")
            print(f"   - Bench employees: {stats['bench_count']} ({stats['bench_percentage']}%)")
            print(f"   - Allocated employees: {stats['allocated_count']}")
            return True
        else:
            print("❌ Failed to load Excel data")
            return False
    except Exception as e:
        print(f"❌ Error loading Excel data: {e}")
        return False

initialize_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global processor, current_data
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and file.filename.endswith('.xlsx'):
            temp_path = f'/tmp/{file.filename}'
            file.save(temp_path)
            
            processor = BenchAnalyticsProcessor(temp_path)
            if processor.load_data():
                current_data = processor.df
                stats = processor.get_basic_stats()
                return jsonify({
                    'success': True,
                    'message': f'File uploaded successfully! {stats["total_employees"]} employees loaded.',
                    'stats': stats
                })
            else:
                return jsonify({'error': 'Failed to process Excel file'}), 400
        else:
            return jsonify({'error': 'Please upload an Excel (.xlsx) file'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/generate_sample')
def generate_sample():
    global processor, current_data
    
    try:
        if initialize_data():
            stats = processor.get_basic_stats()
            return jsonify({
                'success': True,
                'message': f'Real data loaded! {stats["total_employees"]} employees from Excel file.',
                'stats': stats
            })
        else:
            return jsonify({'error': 'Failed to load Excel data'}), 500
    except Exception as e:
        return jsonify({'error': f'Failed to load Excel data: {str(e)}'}), 500

@app.route('/analytics/<chart_type>')
def get_analytics(chart_type):
    global processor, current_data
    
    if processor is None or current_data is None:
        return jsonify({'error': 'No data available. Please upload a file or generate sample data.'}), 400
    
    categories_param = request.args.get('categories', '')
    selected_categories = categories_param.split(',') if categories_param else []
    
    try:
        if chart_type == 'overview':
            return get_overview_charts(selected_categories)
        elif chart_type == 'demographics':
            return get_demographics_charts(selected_categories)
        elif chart_type == 'bench':
            return get_bench_charts(selected_categories)
        elif chart_type == 'skills':
            return get_skills_charts(selected_categories)
        elif chart_type == 'locations':
            return get_locations_charts(selected_categories)
        else:
            return jsonify({'error': 'Invalid chart type'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Failed to generate {chart_type} analytics: {str(e)}'}), 500

def get_overview_charts(selected_categories=None):
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
        
    df = filter_by_categories(current_data, selected_categories)
    
    category_text = f"({', '.join(selected_categories)})" if selected_categories else "(All Categories)"
    
    if 'Designation' in df.columns:
        designation_df = df[df['Designation'].notna() & (df['Designation'] != '') & (df['Designation'] != 'N/A')]
        
        if len(designation_df) > 0:
            designation_counts = designation_df['Designation'].value_counts()
            fig = go.Figure(data=[go.Pie(labels=designation_counts.index.tolist(), values=designation_counts.values.tolist())])
            fig.update_layout(title=f"Designation Distribution {category_text}", height=500)
        else:
            fig = go.Figure()
            fig.update_layout(title=f"Designation Distribution - No Designation Data Available {category_text}", height=500)
            fig.add_annotation(text="No designation assignments found for selected categories", 
                             xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
    else:
        fig = go.Figure()
        fig.update_layout(title=f"Designation Distribution - Designation Column Not Found {category_text}", height=500)
        fig.add_annotation(text="Designation column not available in data", 
                         xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
    
    return jsonify({
        'charts': [
            {'id': 'designation_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))}
        ]
    })

def get_demographics_charts(selected_categories=None):
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
        
    df = filter_by_categories(current_data, selected_categories)
    
    if len(df) == 0:
        return jsonify({'message': 'No employees found for the selected categories'})
    
    category_text = f"({', '.join(selected_categories)})" if selected_categories else "(All Categories)"
    
    gender_counts = df['Gender'].value_counts()
    fig1 = go.Figure(data=[go.Pie(labels=gender_counts.index.tolist(), values=gender_counts.values.tolist())])
    fig1.update_layout(title=f"Gender Distribution {category_text}", height=400)
    
    level_counts = df['Level'].value_counts()
    fig2 = go.Figure(data=[go.Bar(x=level_counts.index.tolist(), y=level_counts.values.tolist())])
    fig2.update_layout(title=f"Employee Level Distribution {category_text}", height=400)
    
    fig3 = go.Figure(data=[go.Histogram(x=df['Total Experience'], nbinsx=20)])
    fig3.update_layout(title=f"Experience Distribution {category_text}", height=400)
    
    return jsonify({
        'charts': [
            {'id': 'gender_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig1))},
            {'id': 'level_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig2))},
            {'id': 'experience_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig3))}
        ]
    })

def get_bench_charts(selected_categories=None):
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
        
    df = filter_by_categories(current_data, selected_categories)
    
    if len(df) == 0:
        return jsonify({'message': 'No employees found for the selected categories'})
    
    category_text = f"({', '.join(selected_categories)})" if selected_categories else "(All Categories)"
    
    if 'Bench Category' in df.columns:
        category_counts = df['Bench Category'].value_counts()
        fig1 = go.Figure(data=[go.Pie(labels=category_counts.index.tolist(), values=category_counts.values.tolist())])
        fig1.update_layout(title=f"Bench Category Distribution {category_text}", height=400)
    else:
        fig1 = go.Figure()
        fig1.update_layout(title=f"Bench Category Distribution - No Data Available {category_text}", height=400)
    
    if 'Current Ageing' in df.columns:
        ageing_ranges = {
            '0-2 weeks': len(df[df['Current Ageing'] <= 14]),
            '2-4 weeks': len(df[(df['Current Ageing'] > 14) & (df['Current Ageing'] <= 28)]),
            '4-8 weeks': len(df[(df['Current Ageing'] > 28) & (df['Current Ageing'] <= 56)]),
            '8+ weeks': len(df[df['Current Ageing'] > 56])
        }
        fig2 = go.Figure(data=[go.Bar(x=list(ageing_ranges.keys()), y=list(ageing_ranges.values()))])
        fig2.update_layout(title=f"Bench Ageing Distribution {category_text}", height=400)
    else:
        fig2 = go.Figure()
        fig2.update_layout(title=f"Bench Ageing Distribution - No Data Available {category_text}", height=400)
    
    return jsonify({
        'charts': [
            {'id': 'bench_category_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig1))},
            {'id': 'bench_ageing_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig2))}
        ]
    })

def get_skills_charts(selected_categories=None):
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
        
    df = filter_by_categories(current_data, selected_categories)
    
    if len(df) == 0:
        return jsonify({'message': 'No employees found for the selected categories'})
    
    category_text = f"({', '.join(selected_categories)})" if selected_categories else "(All Categories)"
    
    skill_counts = df['Tech1 Primary Skill'].value_counts().head(15)
    fig1 = go.Figure(data=[go.Bar(x=skill_counts.index.tolist(), y=skill_counts.values.tolist())])
    fig1.update_layout(title=f"Top 15 Primary Skills {category_text}", height=400)
    
    rag_counts = df['Associate RAG Status'].value_counts()
    colors = {'Green': 'green', 'Amber': 'orange', 'Red': 'red'}
    fig2 = go.Figure(data=[go.Pie(labels=rag_counts.index.tolist(), values=rag_counts.values.tolist())])
    fig2.update_layout(title=f"Associate RAG Status Distribution {category_text}", height=400)
    
    return jsonify({
        'charts': [
            {'id': 'skills_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig1))},
            {'id': 'rag_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig2))}
        ]
    })

def get_locations_charts(selected_categories=None):
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
        
    df = filter_by_categories(current_data, selected_categories)
    
    if len(df) == 0:
        return jsonify({'message': 'No employees found for the selected categories'})
    
    category_text = f"({', '.join(selected_categories)})" if selected_categories else "(All Categories)"
    
    region_counts = df['Location'].value_counts().head(10)
    fig = go.Figure(data=[go.Bar(x=region_counts.index.tolist(), y=region_counts.values.tolist())])
    fig.update_layout(title=f"Top 10 Regions {category_text}", height=400)
    
    return jsonify({
        'charts': [
            {'id': 'region_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))}
        ]
    })

@app.route('/data_preview')
def data_preview():
    global current_data
    
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
    
    categories_param = request.args.get('categories', '')
    selected_categories = categories_param.split(',') if categories_param else []
    
    df = filter_by_categories(current_data, selected_categories)
    
    if len(df) == 0:
        return jsonify({'message': 'No employees found for the selected categories'})
    
    display_columns = ['Employee Code', 'Employee Name', 'Gender', 'Level', 
                      'Location', 'Status', 'Tech1 Primary Skill', 'Total Experience']
    
    available_columns = [col for col in display_columns if col in df.columns]
    preview_data = df[available_columns].head(100)
    
    return jsonify({
        'columns': available_columns,
        'data': preview_data.to_dict('records'),
        'total_rows': len(df)
    })

@app.route('/drill_down')
def drill_down():
    global current_data
    
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
    
    chart_id = request.args.get('chart_id')
    filter_value = request.args.get('filter_value')
    additional_filter = request.args.get('additional_filter')
    
    sort_column = request.args.get('sort_column', 'Employee Name')
    sort_direction = request.args.get('sort_direction', 'asc')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 25))
    visible_columns = request.args.get('visible_columns', '').split(',') if request.args.get('visible_columns') else None
    search_term = request.args.get('search_term', '')
    export_format = request.args.get('export_format')
    
    chart_column_map = {
        'status_chart': 'Status',
        'location_chart': 'Location',
        'region_chart': 'Location', 
        'gender_chart': 'Gender',
        'level_chart': 'Level',
        'bench_category_chart': 'Bench Category',
        'skills_chart': 'Tech1 Primary Skill',
        'rag_chart': 'Associate RAG Status',
        'designation_chart': 'Designation'
    }
    
    try:
        categories_param = request.args.get('categories', '')
        selected_categories = categories_param.split(',') if categories_param else []
        df = filter_by_categories(current_data, selected_categories)
        
        if chart_id == 'experience_chart':
            exp_value = float(filter_value)
            df = df[(df['Total Experience'] >= exp_value-0.5) & (df['Total Experience'] < exp_value+0.5)]
        elif chart_id == 'bench_ageing_chart':
            if filter_value == '0-2 weeks':
                df = df[df['Current Ageing'] <= 14]
            elif filter_value == '2-4 weeks':
                df = df[(df['Current Ageing'] > 14) & (df['Current Ageing'] <= 28)]
            elif filter_value == '4-8 weeks':
                df = df[(df['Current Ageing'] > 28) & (df['Current Ageing'] <= 56)]
            elif filter_value == '8+ weeks':
                df = df[df['Current Ageing'] > 56]
        elif chart_id == 'location_status_chart':
            df = df[df['Location'] == filter_value]
            if additional_filter:
                df = df[df['Status'] == additional_filter]
        else:
            column = chart_column_map.get(chart_id)
            if column and column in df.columns:
                df = df[df[column] == filter_value]
        
        display_columns = ['Employee Name', 'Designation', 'Employment Status', 
                         'Date of Joining', 'Status', 'Client Name', 'Project Name']
        
        all_available_columns = display_columns + ['ATL Eligible', 'Resignation Status', 'Potential ATL']
        available_columns = [col for col in all_available_columns if col in df.columns]
        
        if visible_columns:
            visible_columns = [col for col in visible_columns if col in available_columns]
            result_df = df[visible_columns] if visible_columns else df[display_columns]
        else:
            default_visible = [col for col in display_columns if col in df.columns]
            result_df = df[default_visible]
            visible_columns = default_visible
        
        if search_term:
            search_mask = result_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)
            ).any(axis=1)
            result_df = result_df[search_mask]
        
        if sort_column in result_df.columns:
            ascending = sort_direction.lower() == 'asc'
            result_df = result_df.sort_values(by=sort_column, ascending=ascending)
        
        
        if export_format in ['csv', 'excel']:
            if export_format == 'csv':
                output = io.StringIO()
                result_df.to_csv(output, index=False)
                output.seek(0)
                return Response(
                    output.getvalue(),
                    mimetype='text/csv',
                    headers={'Content-Disposition': f'attachment; filename=employees_{filter_value}.csv'}
                )
            elif export_format == 'excel':
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    result_df.to_excel(writer, index=False, sheet_name='Employees')
                output.seek(0)
                return Response(
                    output.getvalue(),
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    headers={'Content-Disposition': f'attachment; filename=employees_{filter_value}.xlsx'}
                )
        
        total_count = len(result_df)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_df = result_df.iloc[start_idx:end_idx]
        
        return jsonify({
            'success': True,
            'data': paginated_df.to_dict('records'),
            'columns': visible_columns,
            'available_columns': available_columns,
            'total_count': total_count,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size,
            'sort_column': sort_column,
            'sort_direction': sort_direction,
            'filter_info': {
                'chart_id': chart_id,
                'filter_value': filter_value,
                'additional_filter': additional_filter
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Drill-down failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
