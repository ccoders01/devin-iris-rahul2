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
        elif chart_type == 'trends':
            return get_trends_charts(selected_categories)
        elif chart_type == 'opportunities':
            return get_opportunities_charts(selected_categories)
        elif chart_type == 'skills':
            return get_skills_charts(selected_categories)
        elif chart_type == 'locations':
            return get_locations_charts(selected_categories)
        elif chart_type == 'bench_source':
            return get_bench_source_charts(selected_categories)
        elif chart_type == 'ageing':
            return get_ageing_charts(selected_categories)
        else:
            return jsonify({'error': 'Invalid chart type'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Failed to generate {chart_type} analytics: {str(e)}'}), 500

def get_overview_charts(selected_categories=None):
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
        
    df = filter_by_categories(current_data, selected_categories)
    
    category_text = f"({', '.join(selected_categories)})" if selected_categories else "(All Categories)"
    
    if 'Level' in df.columns:
        level_df = df[df['Level'].notna() & (df['Level'] != '') & (df['Level'] != 'N/A')]
        
        if len(level_df) > 0:
            level_counts = level_df['Level'].value_counts()
            fig = go.Figure(data=[go.Pie(labels=level_counts.index.tolist(), values=level_counts.values.tolist())])
            fig.update_layout(title=f"Level Distribution {category_text}", height=500)
        else:
            fig = go.Figure()
            fig.update_layout(title=f"Level Distribution - No Level Data Available {category_text}", height=500)
            fig.add_annotation(text="No level assignments found for selected categories", 
                             xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
    else:
        fig = go.Figure()
        fig.update_layout(title=f"Level Distribution - Level Column Not Found {category_text}", height=500)
        fig.add_annotation(text="Level column not available in data", 
                         xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
    
    return jsonify({
        'charts': [
            {'id': 'level_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))}
        ]
    })

def get_trends_charts(selected_categories=None):
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
        
    df = filter_by_categories(current_data, selected_categories)
    
    if len(df) == 0:
        return jsonify({'message': 'No employees found for the selected categories'})
    
    category_text = f"({', '.join(selected_categories)})" if selected_categories else "(All Categories)"
    
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
            title=f"Employee Progression Through Ageing Slabs {category_text}", 
            height=400,
            xaxis_title="Ageing Slab",
            yaxis_title="Employee Count",
            xaxis=dict(tickangle=45),
            showlegend=False
        )
    else:
        fig1 = go.Figure()
        fig1.update_layout(title=f"Ageing Trends - Actual Ageing Slab Column Not Found {category_text}", height=400)
    
    if 'Planned ReleaseDate' in current_data.columns:
        valid_dates = pd.to_datetime(current_data['Planned ReleaseDate'], errors='coerce')
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
    
    return jsonify({
        'charts': [
            {'id': 'trends_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig1))},
            {'id': 'projected_bench_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig2))}
        ]
    })

def get_opportunities_charts(selected_categories=None):
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
        
    df = filter_by_categories(current_data, selected_categories)
    
    if len(df) == 0:
        return jsonify({'message': 'No employees found for the selected categories'})
    
    category_text = f"({', '.join(selected_categories)})" if selected_categories else "(All Categories)"
    
    if 'Available for Other BU' in df.columns:
        opportunity_counts = df['Available for Other BU'].value_counts()
        fig1 = go.Figure(data=[go.Pie(labels=opportunity_counts.index.tolist(), values=opportunity_counts.values.tolist())])
        fig1.update_layout(title=f"Opportunities Distribution {category_text}", height=400)
    else:
        fig1 = go.Figure()
        fig1.update_layout(title=f"Opportunities Distribution - No Data Available {category_text}", height=400)
    
    return jsonify({
        'charts': [
            {'id': 'opportunities_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig1))}
        ]
    })

def get_skills_charts(selected_categories=None):
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
        
    df = filter_by_categories(current_data, selected_categories)
    
    if len(df) == 0:
        return jsonify({'message': 'No employees found for the selected categories'})
    
    category_text = f"({', '.join(selected_categories)})" if selected_categories else "(All Categories)"
    
    if 'Training Plan' in df.columns:
        training_counts = df['Training Plan'].value_counts()
        fig1 = go.Figure(data=[go.Pie(labels=training_counts.index.tolist(), values=training_counts.values.tolist())])
        fig1.update_layout(title=f"Training Plan Distribution {category_text}", height=400)
    else:
        fig1 = go.Figure()
        fig1.update_layout(title=f"Training Plan Distribution - No Data Available {category_text}", height=400)
    
    rag_counts = df['Associate RAG Status'].value_counts()
    colors = {'Green': 'green', 'Amber': 'orange', 'Red': 'red'}
    fig2 = go.Figure(data=[go.Pie(labels=rag_counts.index.tolist(), values=rag_counts.values.tolist())])
    fig2.update_layout(title=f"Associate RAG Status Distribution {category_text}", height=400)
    
    return jsonify({
        'charts': [
            {'id': 'training_plan_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig1))},
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
    
    if 'State' in df.columns:
        state_counts = df['State'].value_counts()
        fig = go.Figure(data=[go.Pie(labels=state_counts.index.tolist(), values=state_counts.values.tolist())])
        fig.update_layout(title=f"Location Distribution by State {category_text}", height=400)
    else:
        fig = go.Figure()
        fig.update_layout(title=f"Location Distribution - No State Data Available {category_text}", height=400)
    
    return jsonify({
        'charts': [
            {'id': 'location_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))}
        ]
    })

def get_bench_source_charts(selected_categories=None):
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
        
    df = filter_by_categories(current_data, selected_categories)
    
    if len(df) == 0:
        return jsonify({'message': 'No employees found for the selected categories'})
    
    category_text = f"({', '.join(selected_categories)})" if selected_categories else "(All Categories)"
    
    if 'Hired_Released' in df.columns:
        source_counts = df['Hired_Released'].value_counts()
        fig = go.Figure(data=[go.Pie(labels=source_counts.index.tolist(), values=source_counts.values.tolist())])
        fig.update_layout(title=f"Bench Source Distribution {category_text}", height=400)
    else:
        fig = go.Figure()
        fig.update_layout(title=f"Bench Source Distribution - No Data Available {category_text}", height=400)
    
    return jsonify({
        'charts': [
            {'id': 'bench_source_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))}
        ]
    })

def get_ageing_charts(selected_categories=None):
    if current_data is None:
        return jsonify({'error': 'No data available'}), 400
        
    df = filter_by_categories(current_data, selected_categories)
    
    if len(df) == 0:
        return jsonify({'message': 'No employees found for the selected categories'})
    
    category_text = f"({', '.join(selected_categories)})" if selected_categories else "(All Categories)"
    
    if 'Actual Ageing' in df.columns:
        ageing_weeks = {}
        for _, row in df.iterrows():
            days = row['Actual Ageing']
            if pd.notna(days) and days >= 0:
                week_num = int((days - 1) // 7) + 1
                week_label = f"Week {week_num}"
                ageing_weeks[week_label] = ageing_weeks.get(week_label, 0) + 1
        
        if ageing_weeks:
            sorted_weeks = sorted(ageing_weeks.items(), key=lambda x: int(x[0].split()[1]))
            labels, values = zip(*sorted_weeks)
            fig = go.Figure(data=[go.Pie(labels=list(labels), values=list(values))])
            fig.update_layout(title=f"Ageing Distribution (Weeks) {category_text}", height=500)
        else:
            fig = go.Figure()
            fig.update_layout(title=f"Ageing Distribution - No Data Available {category_text}", height=500)
    else:
        fig = go.Figure()
        fig.update_layout(title=f"Ageing Distribution - Actual Ageing Column Not Found {category_text}", height=500)
    
    return jsonify({
        'charts': [
            {'id': 'ageing_chart', 'data': json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))}
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
        'location_chart': 'State',
        'opportunities_chart': 'Available for Other BU',
        'bench_source_chart': 'Hired_Released',
        'training_plan_chart': 'Training Plan',
        'rag_chart': 'Associate RAG Status',
        'ageing_chart': 'Actual Ageing',
        'trends_chart': 'Actual Ageing Slab',
        'projected_bench_chart': 'Planned ReleaseDate'
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
        elif chart_id == 'ageing_chart':
            week_num = int(filter_value.split()[1])
            start_day = (week_num - 1) * 7 + 1
            end_day = week_num * 7
            df = df[(df['Actual Ageing'] >= start_day) & (df['Actual Ageing'] <= end_day)]
        elif chart_id == 'location_status_chart':
            df = df[df['Location'] == filter_value]
            if additional_filter:
                df = df[df['Status'] == additional_filter]
        elif chart_id == 'projected_bench_chart':
            try:
                month_year = pd.to_datetime(filter_value, format='%b %Y')
                
                df['Planned ReleaseDate_parsed'] = pd.to_datetime(df['Planned ReleaseDate'], errors='coerce')
                df = df[df['Planned ReleaseDate_parsed'].notna()]
                
                df = df[
                    (df['Planned ReleaseDate_parsed'].dt.year == month_year.year) &
                    (df['Planned ReleaseDate_parsed'].dt.month == month_year.month)
                ]
                
                df = df.drop('Planned ReleaseDate_parsed', axis=1)
                
            except (ValueError, TypeError) as e:
                df = df.iloc[0:0]
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
