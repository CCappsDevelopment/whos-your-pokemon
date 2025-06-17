#!/usr/bin/env python3
"""
Cross-Platform Build Coordinator
Creates builds for all platforms and packages them for distribution
"""

import os
import shutil
import zipfile
import tarfile
from pathlib import Path
import subprocess
import json
from datetime import datetime

def get_version_info():
    """Get version information for the build"""
    return {
        "version": "2.0",
        "build_date": datetime.now().isoformat(),
        "features": [
            "Manual Pokemon grid setup",
            "Enhanced autocomplete with sprites", 
            "Local image caching",
            "Cross-platform compatibility",
            "1,280+ Pokemon with variants"
        ]
    }

def create_build_info():
    """Create build information file"""
    version_info = get_version_info()
    
    build_info = f"""# Who's Your Pokemon - Build Information

**Version**: {version_info['version']}
**Build Date**: {version_info['build_date']}
**Platforms**: macOS, Windows, Linux

## Features Included
{chr(10).join(['- ' + feature for feature in version_info['features']])}

## Platform-Specific Files

### macOS
- `Whos Your Pokemon.app` - Double-click to run
- Size: ~63MB
- Requirements: macOS 10.14+

### Windows
- `build_windows.bat` - Run this script on Windows to build
- Requirements: Windows 10+, Python 3.7+
- Output: `Whos Your Pokemon.exe`

### Linux  
- `build_linux.sh` - Run this script on Linux to build
- Requirements: Ubuntu 18.04+ or equivalent, Python 3.7+
- Output: `Whos Your Pokemon` executable

## Cross-Platform Improvements
- Platform-aware fonts (Helvetica/Segoe UI/DejaVu Sans)
- Cross-platform mouse wheel scrolling
- Native keyboard shortcuts per platform
- DPI awareness for high-resolution displays
- Robust window management with fallbacks

## Installation Instructions
See CROSS_PLATFORM_BUILD.md for detailed build instructions for each platform.
"""
    
    with open("dist/BUILD_INFO.md", "w") as f:
        f.write(build_info)
    
    # Also create a JSON version for programmatic access
    with open("dist/build_info.json", "w") as f:
        json.dump(version_info, f, indent=2)

def package_source_for_other_platforms():
    """Package source code for building on other platforms"""
    
    # Create a distribution source directory
    dist_src = Path("dist/source")
    if dist_src.exists():
        shutil.rmtree(dist_src)
    dist_src.mkdir(exist_ok=True)
    
    # Files and directories to include in source distribution
    source_items = [
        "src/",
        "assets/",
        "data_sources/",
        "build_tools/",
        "main.py",
        "requirements.txt", 
        "README.md",
        "ARCHITECTURE.md",
        "CROSS_PLATFORM_IMPROVEMENTS.md",
        "CROSS_PLATFORM_SUMMARY.md",
        "build_tools/CROSS_PLATFORM_BUILD.md"
    ]
    
    print("📦 Packaging source code for other platforms...")
    
    for item in source_items:
        try:
            src_path = Path(item)
            if src_path.exists():
                dst_path = dist_src / item
                
                if src_path.is_dir():
                    if dst_path.exists():
                        shutil.rmtree(dst_path)
                    shutil.copytree(src_path, dst_path)
                    print(f"   📁 Copied directory: {item}")
                else:
                    dst_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_path, dst_path)
                    print(f"   📄 Copied file: {item}")
            else:
                print(f"   ⚠️  Not found: {item}")
        except Exception as e:
            print(f"   ❌ Error copying {item}: {e}")
            continue

def create_windows_build_package():
    """Create Windows build package"""
    print("\n🪟 Creating Windows build package...")
    
    windows_dir = Path("dist/windows_build")
    windows_dir.mkdir(exist_ok=True)
    
    # Copy source
    src_dir = windows_dir / "source"
    if src_dir.exists():
        shutil.rmtree(src_dir)
    shutil.copytree("dist/source", src_dir)
    
    # Create Windows-specific build script
    build_script = '''@echo off
REM Who's Your Pokemon - Windows Build Script
echo ============================================================
echo Building Who's Your Pokemon for Windows
echo ============================================================

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.7+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Run the Windows build script
echo 🔨 Building application...
call build_tools\\build_windows.bat

echo ✅ Build complete! Check the dist folder.
pause
'''
    
    with open(windows_dir / "BUILD.bat", "w") as f:
        f.write(build_script)
    
    # Create instructions
    instructions = '''# Windows Build Instructions

1. **Install Python 3.7+** from https://www.python.org/downloads/
2. **Extract this package** to a folder on your computer
3. **Open Command Prompt** in the extracted folder
4. **Run**: `BUILD.bat`
5. **Wait** for the build to complete
6. **Find your app** in the `source/dist` folder

## Manual Build (Alternative)

If the automated script doesn't work:

```cmd
cd source
pip install -r requirements.txt
build_tools\\build_windows.bat
```

## Requirements
- Windows 10 or later
- Python 3.7 or later
- Internet connection (for first-time setup)

## Output
- Executable: `source/dist/Whos Your Pokemon/Whos Your Pokemon.exe`
- Size: ~95MB (includes all Pokemon images)
'''
    
    with open(windows_dir / "WINDOWS_BUILD_INSTRUCTIONS.md", "w") as f:
        f.write(instructions)

def create_linux_build_package():
    """Create Linux build package"""
    print("\n🐧 Creating Linux build package...")
    
    linux_dir = Path("dist/linux_build")
    linux_dir.mkdir(exist_ok=True)
    
    # Copy source
    src_dir = linux_dir / "source"
    if src_dir.exists():
        shutil.rmtree(src_dir)
    shutil.copytree("dist/source", src_dir)
    
    # Create Linux-specific build script
    build_script = '''#!/bin/bash
# Who's Your Pokemon - Linux Build Script
echo "============================================================"
echo "Building Who's Your Pokemon for Linux"
echo "============================================================"

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.7+ first."
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip python3-tk"
    echo "Fedora: sudo dnf install python3 python3-pip python3-tkinter"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Make build script executable
chmod +x build_tools/build_linux.sh

# Run the Linux build script
echo "🔨 Building application..."
./build_tools/build_linux.sh

echo "✅ Build complete! Check the dist folder."
'''
    
    with open(linux_dir / "build.sh", "w") as f:
        f.write(build_script)
    
    # Make it executable
    os.chmod(linux_dir / "build.sh", 0o755)
    
    # Create instructions
    instructions = '''# Linux Build Instructions

## Quick Start

1. **Extract this package** to a folder
2. **Open terminal** in the extracted folder
3. **Run**: `./build.sh`
4. **Wait** for the build to complete
5. **Find your app** in the `source/dist` folder

## Manual Build (Alternative)

```bash
cd source
pip3 install -r requirements.txt
chmod +x build_tools/build_linux.sh
./build_tools/build_linux.sh
```

## Requirements

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

### Fedora/RHEL
```bash
sudo dnf install python3 python3-pip python3-tkinter
```

### Arch Linux
```bash
sudo pacman -S python python-pip tk
```

## Output
- Executable: `source/dist/Whos Your Pokemon/Whos Your Pokemon`
- Launcher: `source/dist/Whos Your Pokemon/run_game.sh`
- Size: ~90MB (includes all Pokemon images)

## Testing
After building, test with:
```bash
cd source/dist/Whos\ Your\ Pokemon/
./Whos\ Your\ Pokemon
```
'''
    
    with open(linux_dir / "LINUX_BUILD_INSTRUCTIONS.md", "w") as f:
        f.write(instructions)

def create_distribution_packages():
    """Create distribution packages for each platform"""
    print("\n📦 Creating distribution packages...")
    
    # Create macOS package (just the .app)
    print("   🍎 Creating macOS package...")
    macos_zip = "dist/WhosYourPokemon_macOS_v2.0.zip"
    with zipfile.ZipFile(macos_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add the .app bundle
        app_path = Path("dist/Whos Your Pokemon.app")
        for file_path in app_path.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(Path("dist"))
                zf.write(file_path, arcname)
        
        # Add build info
        zf.write("dist/BUILD_INFO.md", "BUILD_INFO.md")
    
    print(f"   ✅ Created: {macos_zip}")
    
    # Create Windows package
    print("   🪟 Creating Windows package...")
    windows_zip = "dist/WhosYourPokemon_Windows_v2.0.zip"
    with zipfile.ZipFile(windows_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        windows_dir = Path("dist/windows_build")
        for file_path in windows_dir.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(Path("dist/windows_build"))
                zf.write(file_path, arcname)
    
    print(f"   ✅ Created: {windows_zip}")
    
    # Create Linux package  
    print("   🐧 Creating Linux package...")
    linux_tar = "dist/WhosYourPokemon_Linux_v2.0.tar.gz"
    with tarfile.open(linux_tar, 'w:gz') as tf:
        linux_dir = Path("dist/linux_build")
        for file_path in linux_dir.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(Path("dist/linux_build"))
                tf.add(file_path, arcname)
    
    print(f"   ✅ Created: {linux_tar}")

def main():
    """Main build coordination function"""
    print("=" * 60)
    print("🌍 WHO'S YOUR POKEMON - CROSS-PLATFORM BUILD")
    print("=" * 60)
    
    # Ensure we have a dist directory
    Path("dist").mkdir(exist_ok=True)
    
    # Create build info
    print("📋 Creating build information...")
    create_build_info()
    
    # Package source code
    package_source_for_other_platforms()
    
    # Create platform-specific packages
    create_windows_build_package()
    create_linux_build_package()
    
    # Create distribution packages
    create_distribution_packages()
    
    # Show summary
    print("\n" + "=" * 60)
    print("🎉 CROSS-PLATFORM BUILD COMPLETE!")
    print("=" * 60)
    
    print("\n📱 **macOS Build (Ready to Use)**:")
    print("   • dist/Whos Your Pokemon.app (63MB)")
    print("   • Double-click to run on macOS 10.14+")
    
    print("\n📦 **Distribution Packages**:")
    
    dist_files = [
        "WhosYourPokemon_macOS_v2.0.zip",
        "WhosYourPokemon_Windows_v2.0.zip", 
        "WhosYourPokemon_Linux_v2.0.tar.gz"
    ]
    
    for package in dist_files:
        package_path = Path(f"dist/{package}")
        if package_path.exists():
            size = package_path.stat().st_size / (1024 * 1024)
            print(f"   • {package} ({size:.1f}MB)")
    
    print("\n🔧 **Build Instructions Included**:")
    print("   • Windows: BUILD.bat + detailed instructions")
    print("   • Linux: build.sh + detailed instructions")
    print("   • Cross-platform source code included")
    
    print("\n✨ **Cross-Platform Features**:")
    print("   • Native fonts for each platform")
    print("   • Platform-specific keyboard shortcuts")
    print("   • Cross-platform mouse wheel support")
    print("   • DPI awareness for high-res displays")
    print("   • Robust window management")
    
    print("\n🚀 **Ready for Distribution!**")
    print("=" * 60)

if __name__ == "__main__":
    main()
