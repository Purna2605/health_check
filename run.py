#!/usr/bin/env python3
"""
Startup script for Health Check App
"""

if __name__ == "__main__":
    from app import app
    print("🏥 Starting Health Check App...")
    print("📱 Open http://localhost:5000 in your browser")
    print("⏹️  Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)