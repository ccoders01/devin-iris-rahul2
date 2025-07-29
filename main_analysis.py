import os
import pandas as pd
import matplotlib.pyplot as plt
from data_processor import BenchAnalyticsProcessor
from visualizations import BenchAnalyticsVisualizer

def main():
    file_path = '/home/ubuntu/attachments/8a127e00-2a79-4984-bcf6-6a45b5ebcfeb/TestcolumnOnly_Bench+capacity+Jun+24.xlsx'
    
    processor = BenchAnalyticsProcessor(file_path)
    
    print("=== BENCH ANALYTICS REPORT ===\n")
    
    if processor.load_data():
        print("✓ Excel file loaded successfully")
        print(f"  - Shape: {processor.df.shape}")
        print(f"  - Columns: {len(processor.df.columns)}")
        
        if len(processor.df) == 0:
            print("\n⚠️  The Excel file contains only column headers with no data rows.")
            print("   Generating sample data for demonstration purposes...\n")
            processor.generate_sample_data(500)
    else:
        print("❌ Failed to load Excel file. Generating sample data...")
        processor.generate_sample_data(500)
    
    visualizer = BenchAnalyticsVisualizer(processor)
    
    os.makedirs('/home/ubuntu/bench_analytics/outputs', exist_ok=True)
    
    print("=== BASIC STATISTICS ===")
    stats = processor.get_basic_stats()
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    
    print("\n=== SKILL DISTRIBUTION ===")
    skills = processor.get_skill_distribution()
    for skill, count in list(skills.items())[:10]:
        print(f"  {skill}: {count}")
    
    print("\n=== LOCATION DISTRIBUTION ===")
    locations = processor.get_location_distribution()
    for location, count in list(locations.items())[:10]:
        print(f"  {location}: {count}")
    
    print("\n=== BENCH ANALYSIS ===")
    bench_analysis = processor.get_bench_analysis()
    if 'message' in bench_analysis:
        print(f"  {bench_analysis['message']}")
    else:
        print(f"  Total Bench: {bench_analysis.get('total_bench', 0)}")
        print(f"  Average Ageing: {bench_analysis.get('avg_ageing', 0):.1f} days")
        
        if 'ageing_ranges' in bench_analysis:
            print("  Ageing Ranges:")
            for range_name, count in bench_analysis['ageing_ranges'].items():
                print(f"    {range_name}: {count}")
    
    print("\n=== GENERATING VISUALIZATIONS ===")
    
    demographics_chart = visualizer.create_employee_demographics_chart(
        '/home/ubuntu/bench_analytics/outputs/demographics_analysis.png'
    )
    
    bench_chart = visualizer.create_bench_analysis_chart(
        '/home/ubuntu/bench_analytics/outputs/bench_analysis.png'
    )
    
    skills_chart = visualizer.create_skills_analysis_chart(
        '/home/ubuntu/bench_analytics/outputs/skills_analysis.png'
    )
    
    allocation_chart = visualizer.create_allocation_analysis_chart(
        '/home/ubuntu/bench_analytics/outputs/allocation_analysis.png'
    )
    
    interactive_fig = visualizer.create_interactive_dashboard()
    if interactive_fig:
        interactive_fig.write_html('/home/ubuntu/bench_analytics/outputs/interactive_dashboard.html')
        print("✓ Interactive dashboard saved as HTML")
    
    print("\n=== COLUMN CATEGORIES ANALYSIS ===")
    categories = processor.column_categories
    for category, columns in categories.items():
        available_cols = [col for col in columns if col in processor.df.columns]
        print(f"\n{category.replace('_', ' ').title()}:")
        print(f"  Available columns: {len(available_cols)}/{len(columns)}")
        if len(available_cols) < len(columns):
            missing = [col for col in columns if col not in processor.df.columns]
            print(f"  Missing columns: {missing[:5]}{'...' if len(missing) > 5 else ''}")
    
    print("\n=== KEY INSIGHTS ===")
    
    if len(processor.df) > 0:
        total_employees = len(processor.df)
        bench_count = len(processor.df[processor.df['Status'] == 'Bench']) if 'Status' in processor.df.columns else 0
        bench_percentage = (bench_count / total_employees * 100) if total_employees > 0 else 0
        
        print(f"• Total workforce: {total_employees:,} employees")
        print(f"• Bench utilization: {bench_percentage:.1f}% ({bench_count} employees)")
        
        if 'Gender' in processor.df.columns:
            gender_dist = processor.df['Gender'].value_counts(normalize=True) * 100
            print(f"• Gender diversity: {gender_dist.to_dict()}")
        
        if 'Location' in processor.df.columns:
            top_location = processor.df['Location'].value_counts().index[0]
            top_location_count = processor.df['Location'].value_counts().iloc[0]
            print(f"• Largest location: {top_location} ({top_location_count} employees)")
        
        if 'Tech1 Primary Skill' in processor.df.columns:
            top_skill = processor.df['Tech1 Primary Skill'].value_counts().index[0]
            top_skill_count = processor.df['Tech1 Primary Skill'].value_counts().iloc[0]
            print(f"• Most common skill: {top_skill} ({top_skill_count} employees)")
    
    print("\n=== RECOMMENDATIONS ===")
    print("• Implement regular bench review meetings to reduce ageing")
    print("• Focus on skill development for high-demand technologies")
    print("• Consider cross-training to improve allocation flexibility")
    print("• Monitor bench trends by location and skill category")
    print("• Establish clear SLAs for bench allocation timelines")
    
    print(f"\n=== OUTPUT FILES ===")
    print("📊 Visualizations saved to: /home/ubuntu/bench_analytics/outputs/")
    print("📈 Interactive dashboard: /home/ubuntu/bench_analytics/outputs/interactive_dashboard.html")
    print("📋 All analysis charts saved as PNG files")
    
    return processor, visualizer

if __name__ == "__main__":
    processor, visualizer = main()
