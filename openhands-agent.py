"""
OpenHands Agent Script - Run this inside OpenHands environment
Purpose: Autonomous monitoring and self-healing of the pipeline
"""

import subprocess
import json
from datetime import datetime
import shutil

def check_website_health():
    """Verify the generated site is valid"""
    try:
        with open("site/index.html", "r") as f:
            content = f.read()
            
        # Check for common failures
        checks = {
            "has_content": len(content) > 1000,
            "has_title": "<title>" in content,
            "not_empty": "{{title}}" not in content,  # Template rendered
            "has_brain_rot": "☕" in content or "no cap" in content
        }
        
        return all(checks.values())
    except Exception as e:
        return False

def self_heal():
    """Attempt to fix common issues autonomously"""
    print("🔧 Running self-healing protocols...")
    
    # Check if uv is available, otherwise fallback to python
    cmd = ["uv", "run", "src/main.py"]
    if not shutil.which("uv"):
        print("⚠️ 'uv' not found, falling back to 'python'")
        cmd = ["python", "src/main.py"]

    # Re-run generator if checks fail
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        # Log error for review
        with open("error.log", "a") as f:
            f.write(f"{datetime.now()}: {result.stderr}\n")
        return False
    
    return True

if __name__ == "__main__":
    if not check_website_health():
        success = self_heal()
        exit(0 if success else 1)
    print("✅ All systems operational")
