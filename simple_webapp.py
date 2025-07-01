#!/usr/bin/env python3
"""
Simple Flask Web Application for Bench Analytics
A more reliable alternative to the Dash implementation
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.utils
import json
import io
import base64
from data_processor import BenchAnalyticsProcessor

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

processor = None
current_data = None

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
        processor = BenchAnalyticsProcessor()
        current_data = processor.generate_sample_data(500)
        stats = processor.get_basic_stats()
        
        return jsonify({
            'success': True,
            'message': f'Sample data generated! {stats["total_employees"]} employees created.',
            'stats': stats
        })
    except Exception as e:
        return jsonify({'error': f'Failed to generate sample data: {str(e)}'}), 500

@app.route('/analytics/<chart_type>')
def get_analytics(chart_type):
    global processor, current_data
    
    if processor is None or current_data is None:
        return jsonify({'error': 'No data available. Please upload a file or generate sample data.'}), 400
    
    try:
        if chart_type == 'overview':
            return get_overview_charts()
        elif chart_type == 'demographics':
            return get_demographics_charts()
        elif chart_type == 'bench':
            return get_bench_charts()
        elif chart_type == 'skills':
            return get_skills_charts()
        elif chart_type == 'locations':
            return get_locations_charts()
        else:
            return jsonify({'error': 'Invalid chart type'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Failed to generate {chart_type} analytics: {str(e)}'}), 500

def get_overview_charts():
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
        
    df = current_data
    
    status_counts = df['Status'].value_counts()
    fig1 = go.Figure(data=[go.Pie(labels=status_counts.index, values=status_counts.values)])
    fig1.update_layout(title="Employee Status Distribution", height=400)
    
    location_counts = df['Location'].value_counts().head(10)
    fig2 = go.Figure(data=[go.Bar(x=location_counts.index, y=location_counts.values)])
    fig2.update_layout(title="Top 10 Locations", height=400)
    
    return jsonify({
        'charts': [
            {'id': 'status_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig1))},
            {'id': 'location_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig2))}
        ]
    })

def get_demographics_charts():
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
        
    df = current_data
    
    gender_counts = df['Gender'].value_counts()
    fig1 = go.Figure(data=[go.Pie(labels=gender_counts.index, values=gender_counts.values)])
    fig1.update_layout(title="Gender Distribution", height=400)
    
    level_counts = df['Level'].value_counts()
    fig2 = go.Figure(data=[go.Bar(x=level_counts.index, y=level_counts.values)])
    fig2.update_layout(title="Employee Level Distribution", height=400)
    
    fig3 = go.Figure(data=[go.Histogram(x=df['Total Experience'], nbinsx=20)])
    fig3.update_layout(title="Experience Distribution", height=400)
    
    return jsonify({
        'charts': [
            {'id': 'gender_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig1))},
            {'id': 'level_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig2))},
            {'id': 'experience_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig3))}
        ]
    })

def get_bench_charts():
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
        
    df = current_data
    bench_df = df[df['Status'] == 'Bench']
    
    if len(bench_df) == 0:
        return jsonify({'message': 'No bench employees found in the data'})
    
    category_counts = bench_df['Bench Category'].value_counts()
    fig1 = go.Figure(data=[go.Pie(labels=category_counts.index, values=category_counts.values)])
    fig1.update_layout(title="Bench Category Distribution", height=400)
    
    ageing_ranges = {
        '0-2 weeks': len(bench_df[bench_df['Current Ageing'] <= 14]),
        '2-4 weeks': len(bench_df[(bench_df['Current Ageing'] > 14) & (bench_df['Current Ageing'] <= 28)]),
        '4-8 weeks': len(bench_df[(bench_df['Current Ageing'] > 28) & (bench_df['Current Ageing'] <= 56)]),
        '8+ weeks': len(bench_df[bench_df['Current Ageing'] > 56])
    }
    
    fig2 = go.Figure(data=[go.Bar(x=list(ageing_ranges.keys()), y=list(ageing_ranges.values()))])
    fig2.update_layout(title="Bench Ageing Distribution", height=400)
    
    return jsonify({
        'charts': [
            {'id': 'bench_category_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig1))},
            {'id': 'bench_ageing_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig2))}
        ]
    })

def get_skills_charts():
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
        
    df = current_data
    
    skill_counts = df['Tech1 Primary Skill'].value_counts().head(15)
    fig1 = go.Figure(data=[go.Bar(x=skill_counts.index, y=skill_counts.values)])
    fig1.update_layout(title="Top 15 Primary Skills", height=400)
    
    rag_counts = df['Associate RAG Status'].value_counts()
    colors = {'Green': 'green', 'Amber': 'orange', 'Red': 'red'}
    fig2 = go.Figure(data=[go.Pie(labels=rag_counts.index, values=rag_counts.values)])
    fig2.update_layout(title="RAG Status Distribution", height=400)
    
    return jsonify({
        'charts': [
            {'id': 'skills_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig1))},
            {'id': 'rag_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig2))}
        ]
    })

def get_locations_charts():
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
        
    df = current_data
    
    location_status = pd.crosstab(df['Location'], df['Status'])
    
    fig = go.Figure()
    for status in location_status.columns:
        fig.add_trace(go.Bar(name=status, x=location_status.index, y=location_status[status]))
    
    fig.update_layout(title="Status Distribution by Location", barmode='stack', height=400)
    
    return jsonify({
        'charts': [
            {'id': 'location_status_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))}
        ]
    })

@app.route('/data_preview')
def data_preview():
    global current_data
    
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
    
    display_columns = ['Employee Code', 'Employee Name', 'Gender', 'Level', 
                      'Location', 'Status', 'Tech1 Primary Skill', 'Total Experience']
    
    available_columns = [col for col in display_columns if col in current_data.columns]
    preview_data = current_data[available_columns].head(100)
    
    return jsonify({
        'columns': available_columns,
        'data': preview_data.to_dict('records'),
        'total_rows': len(current_data)
    })

@app.route('/drill_down')
def drill_down():
    global current_data
    
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
    
    chart_id = request.args.get('chart_id')
    filter_value = request.args.get('filter_value')
    additional_filter = request.args.get('additional_filter')  # For stacked charts
    
    chart_column_map = {
        'status_chart': 'Status',
        'location_chart': 'Location', 
        'gender_chart': 'Gender',
        'level_chart': 'Level',
        'bench_category_chart': 'Bench Category',
        'skills_chart': 'Tech1 Primary Skill',
        'rag_chart': 'Associate RAG Status'
    }
    
    try:
        df = current_data.copy()
        
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
        available_columns = [col for col in display_columns if col in df.columns]
        result_df = df[available_columns]
        
        return jsonify({
            'success': True,
            'data': result_df.to_dict('records'),
            'columns': available_columns,
            'total_count': len(result_df),
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
