#!/usr/bin/env python3
"""
Setup script for EUEE Study Companion

This script helps set up the development environment for the EUEE Study Companion project.
It creates necessary directories, sets up environment files, and provides guidance for next steps.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def create_directory(path):
    """Create a directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"✅ Created directory: {path}")

def copy_file(src, dst):
    """Copy a file if it exists"""
    if Path(src).exists():
        shutil.copy2(src, dst)
        print(f"✅ Copied {src} to {dst}")
    else:
        print(f"⚠️  Source file not found: {src}")

def main():
    print("🎓 EUEE Study Companion - Setup Script")
    print("=" * 50)
    
    # Get the project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("\n📁 Creating project structure...")
    
    # Create necessary directories
    directories = [
        "Backend/uploads",
        "Backend/logs",
        "Frontend/public",
        "Data/books",
        "Data/exams",
        "Docs",
        "Supabase"
    ]
    
    for directory in directories:
        create_directory(directory)
    
    print("\n📄 Setting up environment files...")
    
    # Copy environment example files
    if Path("env.example").exists():
        # Backend .env
        copy_file("env.example", "Backend/.env")
        
        # Frontend .env.local
        copy_file("env.example", "Frontend/.env.local")
    else:
        print("⚠️  env.example not found. Please create it manually.")
    
    print("\n🔧 Checking prerequisites...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 8:
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print("❌ Python 3.8+ is required")
        return
    
    # Check Node.js
    success, stdout, stderr = run_command("node --version")
    if success:
        print(f"✅ Node.js: {stdout.strip()}")
    else:
        print("❌ Node.js is required")
        return
    
    # Check npm
    success, stdout, stderr = run_command("npm --version")
    if success:
        print(f"✅ npm: {stdout.strip()}")
    else:
        print("❌ npm is required")
        return
    
    print("\n🚀 Setup complete! Next steps:")
    print("\n1. Configure environment variables:")
    print("   - Edit Backend/.env")
    print("   - Edit Frontend/.env.local")
    
    print("\n2. Set up the database:")
    print("   - Install PostgreSQL")
    print("   - Create database: createdb euee_study_companion")
    
    print("\n3. Install backend dependencies:")
    print("   cd Backend")
    print("   python -m venv venv")
    print("   source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print("   pip install -r requirements.txt")
    
    print("\n4. Install frontend dependencies:")
    print("   cd Frontend")
    print("   npm install")
    
    print("\n5. Start the development servers:")
    print("   # Backend (in Backend directory)")
    print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    print("   # Frontend (in Frontend directory)")
    print("   npm run dev")
    
    print("\n📚 For more information, see README.md")
    print("\n🎯 Happy coding!")

if __name__ == "__main__":
    main() 