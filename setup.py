#!/usr/bin/env python3
"""
Setup script for AI-Powered Cattle Management Platform
"""

import os
import subprocess
import sys

def create_directories():
    """Create necessary directories"""
    directories = [
        ".streamlit",
        "data",
        "logs",
        "assets"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def setup_secrets():
    """Setup secrets configuration"""
    secrets_file = ".streamlit/secrets.toml"
    if not os.path.exists(secrets_file):
        print(f"\n🔐 Creating secrets configuration...")
        with open(secrets_file, 'w') as f:
            f.write("# Add your Groq API key here\n")
            f.write("GROQ_API_KEY = \"your_groq_api_key_here\"\n")
        print(f"✅ Created {secrets_file}")
        print("⚠️  Please edit this file and add your Groq API key")
    else:
        print(f"📁 Secrets file already exists: {secrets_file}")

def create_sample_data():
    """Create sample data files"""
    sample_data = {
        "data/sample_breeds.json": {
            "breeds": [
                {"name": "Gir", "origin": "Gujarat", "characteristics": "High milk yield, disease resistant"},
                {"name": "Sahiwal", "origin": "Punjab", "characteristics": "Heat tolerant, good milk producer"},
                {"name": "Red Sindhi", "origin": "Sindh", "characteristics": "Adaptable, moderate milk yield"},
                {"name": "Tharparkar", "origin": "Rajasthan", "characteristics": "Drought resistant, dual purpose"},
                {"name": "Kankrej", "origin": "Gujarat", "characteristics": "Strong, good for draught work"}
            ]
        },
        "data/sample_trading.json": {
            "listings": [
                {
                    "id": 1,
                    "breed": "Gir",
                    "age": "3 years",
                    "price": 45000,
                    "location": "Karnataka",
                    "health": "Excellent",
                    "seller": "Ramu Patel",
                    "contact": "+91-9876543210"
                }
            ]
        }
    }
    
    for filename, data in sample_data.items():
        if not os.path.exists(filename):
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            import json
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✅ Created sample data: {filename}")

def main():
    """Main setup function"""
    print("🐄 AI-Powered Cattle Management Platform Setup")
    print("=" * 60)
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed due to package installation errors")
        sys.exit(1)
    
    # Setup secrets
    setup_secrets()
    
    # Create sample data
    create_sample_data()
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .streamlit/secrets.toml and add your Groq API key")
    print("2. Run: python run.py")
    print("3. Open http://localhost:8501 in your browser")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main()
