#!/usr/bin/env python3
"""
Cross-platform build script for Who's Your Pokemon game
Creates builds for macOS, Windows, and Linux using PyInstaller
"""

import os
import subprocess
import sys
import platform
from pathlib import Path
import shutil

def get_platform_info():
    """Get current platform information"""
    system = platform.system().lower()
    return {
        'system': system,
        'is_macos': system == 'darwin',
        'is_windows': system == 'windows',
        'is_linux': system == 'linux'
    }

def build_for_platform(target_platform='current'):
    """Build the application for specified platform"""
    
    # Ensure we're in the parent directory (project root)
    script_dir = Path(__file__).parent.parent
    os.chdir(script_dir)
    
    platform_info = get_platform_info()
    current_system = platform_info['system']
    
    if target_platform == 'current':
        target_platform = current_system
    
    print(f"🔨 Building Who's Your Pokemon for {target_platform.title()}...")
    print(f"Current system: {current_system.title()}")
    
    # Base PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=Whos Your Pokemon",  # App name
        "--windowed",  # No console window
        "--onedir",  # Create a directory with all files
        "--add-data=data_sources/pokemon_data.json:data_sources",  # Include Pokemon data
        "--add-data=assets:assets",  # Include all assets
        "--clean",  # Clean cache before building
        "--noconfirm",  # Overwrite without asking
    ]
    
    # Platform-specific configurations
    if target_platform == 'darwin' or (target_platform == 'current' and platform_info['is_macos']):
        # macOS build
        cmd.extend([
            "--icon=assets/question_mark.icns",  # macOS icon
        ])
        executable_name = "Whos Your Pokemon"
        dist_folder = "dist/Whos Your Pokemon"
        
    elif target_platform == 'windows' or (target_platform == 'current' and platform_info['is_windows']):
        # Windows build
        # First, check if we have a .ico file, if not create one
        ico_path = "assets/question_mark.ico"
        if not Path(ico_path).exists():
            print("📸 Converting icon for Windows...")
            create_windows_icon()
        
        cmd.extend([
            "--icon=assets/question_mark.ico",  # Windows icon
        ])
        executable_name = "Whos Your Pokemon.exe"
        dist_folder = "dist/Whos Your Pokemon"
        
    else:
        # Linux build (no icon needed)
        executable_name = "Whos Your Pokemon"
        dist_folder = "dist/Whos Your Pokemon"
    
    # Add main file
    cmd.append("main.py")
    
    try:
        # Run PyInstaller
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build completed successfully!")
        
        # Print location of built app
        print(f"📦 Application built at: {dist_folder}")
        
        if platform_info['is_macos'] and (target_platform == 'darwin' or target_platform == 'current'):
            # Create .app bundle for macOS
            create_macos_app_bundle()
            print(f"🚀 To run: open 'dist/Whos Your Pokemon.app'")
        elif platform_info['is_windows'] or target_platform == 'windows':
            print(f"🚀 To run: double-click '{dist_folder}/{executable_name}'")
        else:
            print(f"🚀 To run: ./{dist_folder}/{executable_name}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with error:")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def create_windows_icon():
    """Create a Windows .ico file from the PNG icon"""
    try:
        from PIL import Image
        
        # Load the PNG icon
        png_path = "assets/question_mark.png"
        ico_path = "assets/question_mark.ico"
        
        if Path(png_path).exists():
            # Open and convert to ICO
            img = Image.open(png_path)
            # Create multiple sizes for Windows
            sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
            img.save(ico_path, format='ICO', sizes=sizes)
            print(f"✅ Created Windows icon: {ico_path}")
        else:
            print(f"⚠️  PNG icon not found at {png_path}")
            
    except ImportError:
        print("⚠️  Pillow not available for icon conversion")
    except Exception as e:
        print(f"⚠️  Could not create Windows icon: {e}")

def create_macos_app_bundle():
    """Create a proper .app bundle for macOS"""
    
    print("📱 Creating Mac .app bundle...")
    
    # Path to the built executable
    dist_path = Path("dist/Whos Your Pokemon")
    app_path = Path("dist/Whos Your Pokemon.app")
    
    if not dist_path.exists():
        print("❌ Built application not found. Run build first.")
        return False
    
    try:
        # Remove existing app bundle if it exists
        if app_path.exists():
            shutil.rmtree(app_path)
        
        # Create .app bundle structure
        contents_path = app_path / "Contents"
        macos_path = contents_path / "MacOS"
        resources_path = contents_path / "Resources"
        
        # Create directories
        macos_path.mkdir(parents=True, exist_ok=True)
        resources_path.mkdir(parents=True, exist_ok=True)
        
        # Copy the entire dist folder contents to MacOS
        shutil.copytree(dist_path, macos_path, dirs_exist_ok=True)
        
        # Create Info.plist
        info_plist = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>Who's Your Pokemon</string>
    <key>CFBundleExecutable</key>
    <string>Whos Your Pokemon</string>
    <key>CFBundleIconFile</key>
    <string>icon.icns</string>
    <key>CFBundleIdentifier</key>
    <string>com.ccappsdevelopment.whosyourpokemon</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>Whos Your Pokemon</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>2.0</string>
    <key>CFBundleVersion</key>
    <string>2.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.14</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSRequiresAquaSystemAppearance</key>
    <false/>
</dict>
</plist>'''
        
        with open(contents_path / "Info.plist", "w") as f:
            f.write(info_plist)
        
        # Copy icon
        icon_source = Path("assets/question_mark.icns")
        if icon_source.exists():
            shutil.copy2(icon_source, resources_path / "icon.icns")
        
        print("✅ Mac .app bundle created successfully!")
        print(f"📦 App bundle at: {app_path}")
        print("🚀 Double-click the .app to run!")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create .app bundle: {e}")
        return False

def create_windows_installer():
    """Create a Windows installer (if NSIS is available)"""
    print("📦 Creating Windows installer...")
    
    # This would require NSIS (Nullsoft Scriptable Install System)
    # For now, we'll just create a simple batch file to run the app
    
    dist_path = Path("dist/Whos Your Pokemon")
    if not dist_path.exists():
        print("❌ Built application not found.")
        return False
    
    try:
        # Create a simple launcher batch file
        batch_content = '''@echo off
cd /d "%~dp0"
start "" "Whos Your Pokemon.exe"
'''
        with open(dist_path / "Run Game.bat", "w") as f:
            f.write(batch_content)
        
        print("✅ Created Windows launcher: 'Run Game.bat'")
        return True
        
    except Exception as e:
        print(f"⚠️  Could not create Windows launcher: {e}")
        return False

def build_all_platforms():
    """Build for all supported platforms (where possible)"""
    platform_info = get_platform_info()
    
    print("🌍 Building for all platforms...")
    
    # Always build for current platform
    success = build_for_platform('current')
    
    if platform_info['is_macos']:
        print("\n" + "="*50)
        print("ℹ️  Note: Cross-compilation to Windows/Linux from macOS")
        print("requires additional setup and may not work perfectly.")
        print("For best results, build on each target platform.")
        print("="*50)
    
    return success

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Build Who\'s Your Pokemon for multiple platforms')
    parser.add_argument('--platform', choices=['current', 'macos', 'darwin', 'windows', 'linux', 'all'], 
                       default='current', help='Target platform (default: current)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Who's Your Pokemon - Cross-Platform Builder")
    print("=" * 60)
    
    if args.platform == 'all':
        success = build_all_platforms()
    else:
        target = args.platform
        if target in ['macos', 'darwin']:
            target = 'darwin'
        success = build_for_platform(target)
    
    if success:
        platform_info = get_platform_info()
        
        # Platform-specific post-build steps
        if platform_info['is_windows']:
            create_windows_installer()
        
        print("\n" + "=" * 60)
        print("🎉 Build Complete!")
        print("Your app is ready in the 'dist' folder")
        print("=" * 60)
    else:
        print("\n❌ Build failed. Please check the errors above.")
        sys.exit(1)
