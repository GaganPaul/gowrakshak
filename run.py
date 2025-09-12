#!/usr/bin/env python3
"""
AI-Powered Cattle Management Platform Launcher
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import streamlit
        import groq
        import PIL
        import pandas
        import plotly
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_api_key():
    """Check if Groq API key is configured"""
    secrets_file = ".streamlit/secrets.toml"
    if os.path.exists(secrets_file):
        with open(secrets_file, 'r') as f:
            content = f.read()
            if "your_groq_api_key_here" in content:
                print("⚠️  Please configure your Groq API key in .streamlit/secrets.toml")
                return False
            else:
                print("✅ Groq API key is configured")
                return True
    else:
        print("❌ secrets.toml file not found")
        return False

def main():
    """Main launcher function"""
    print("🐄 AI-Powered Cattle Management Platform")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check API key
    if not check_api_key():
        print("\nTo get your Groq API key:")
        print("1. Visit https://console.groq.com/")
        print("2. Sign up for an account")
        print("3. Generate an API key")
        print("4. Add it to .streamlit/secrets.toml")
        sys.exit(1)
    
    print("\n🚀 Starting the application...")
    print("The app will open in your default browser at http://localhost:8501")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Launch Streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
