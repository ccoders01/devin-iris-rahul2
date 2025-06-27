#!/usr/bin/env python3
"""
Bench Analytics Web Application Launcher
Run this script to start the web application
"""

import os
import sys
from web_app import BenchAnalyticsWebApp

def main():
    print("=" * 60)
    print("🎯 BENCH ANALYTICS WEB APPLICATION")
    print("=" * 60)
    print()
    print("📊 Features:")
    print("  • Upload Excel files for analysis")
    print("  • Interactive dashboards and visualizations")
    print("  • Real-time analytics and insights")
    print("  • 152-column workforce data support")
    print()
    print("🚀 Starting application...")
    print()
    
    try:
        app = BenchAnalyticsWebApp()
        app.run(host='0.0.0.0', port=8050, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
