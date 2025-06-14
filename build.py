#!/usr/bin/env python3
"""
Wrapper script to build the application
Calls the build script in build_tools/
"""

import os
import sys
from pathlib import Path

# Change to the project directory
project_dir = Path(__file__).parent
os.chdir(project_dir)

# Run the build script from build_tools
sys.path.insert(0, str(project_dir / "build_tools"))

try:
    from build_app import build_app
    build_app()
except ImportError as e:
    print(f"❌ Error importing build script: {e}")
    print("Make sure build_tools/build_app.py exists")
    sys.exit(1)
