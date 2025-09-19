#!/usr/bin/env python3
"""
J1-CyberThreatAnalyzer Backend Runner
Automatically sets up virtual environment and runs the FastAPI backend
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_python():
    """Check if Python is available"""
    success, stdout, stderr = run_command("python --version")
    if success:
        print(f"✅ Python found: {stdout.strip()}")
        return True
    else:
        print("❌ Python not found. Please install Python 3.12+")
        return False

def setup_virtual_environment():
    """Set up virtual environment if it doesn't exist"""
    venv_path = Path("backend/venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("🔧 Creating virtual environment...")
    success, stdout, stderr = run_command("python -m venv backend/venv")
    
    if success:
        print("✅ Virtual environment created successfully")
        return True
    else:
        print(f"❌ Failed to create virtual environment: {stderr}")
        return False

def get_activation_command():
    """Get the correct activation command based on OS"""
    if platform.system() == "Windows":
        return "backend\\venv\\Scripts\\activate"
    else:
        return "source backend/venv/bin/activate"

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    # Determine the correct pip command
    if platform.system() == "Windows":
        pip_cmd = "backend\\venv\\Scripts\\pip"
    else:
        pip_cmd = "backend/venv/bin/pip"
    
    success, stdout, stderr = run_command(f"{pip_cmd} install -r backend/requirements.txt")
    
    if success:
        print("✅ Dependencies installed successfully")
        return True
    else:
        print(f"❌ Failed to install dependencies: {stderr}")
        return False

def check_ollama():
    """Check if Ollama is running"""
    print("🔍 Checking Ollama connection...")
    success, stdout, stderr = run_command("curl -s http://localhost:11434/api/tags")
    
    if success:
        print("✅ Ollama is running")
        return True
    else:
        print("⚠️  Ollama is not running. Please start Ollama first:")
        print("   ollama serve")
        print("   ollama pull llama3.2:3b")
        return False

def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting J1-CyberThreatAnalyzer backend...")
    
    # Determine the correct python command
    if platform.system() == "Windows":
        python_cmd = "backend\\venv\\Scripts\\python"
    else:
        python_cmd = "backend/venv/bin/python"
    
    print("=" * 60)
    print("🛡️  J1-CyberThreatAnalyzer Backend Starting...")
    print("=" * 60)
    print("📡 API will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🏥 Health Check: http://localhost:8000/health")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Run the backend server
        subprocess.run([python_cmd, "backend/main.py"], cwd=".")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main function to set up and run the backend"""
    print("🛡️  J1-CyberThreatAnalyzer Backend Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("backend/main.py").exists():
        print("❌ Please run this script from the J1-CyberThreatAnalyzer root directory")
        print("   The backend/main.py file should be present")
        return
    
    # Step 1: Check Python
    if not check_python():
        return
    
    # Step 2: Setup virtual environment
    if not setup_virtual_environment():
        return
    
    # Step 3: Install dependencies
    if not install_dependencies():
        return
    
    # Step 4: Check Ollama (optional warning)
    check_ollama()
    
    # Step 5: Start backend
    start_backend()

if __name__ == "__main__":
    main()
