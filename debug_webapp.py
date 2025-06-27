#!/usr/bin/env python3
"""
Debug script to test the web application with better error handling
"""

from web_app import BenchAnalyticsWebApp
import traceback

def main():
    print("🔍 Testing Bench Analytics Web Application...")
    
    try:
        print("📝 Creating app instance...")
        app = BenchAnalyticsWebApp()
        print("✅ App created successfully")
        
        print("🚀 Starting server...")
        app.run(debug=True, host='0.0.0.0', port=8050)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("📋 Full traceback:")
        traceback.print_exc()

if __name__ == '__main__':
    main()
