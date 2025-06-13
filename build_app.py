#!/usr/bin/env python3
"""
Build script for Who's Your Pokemon game
Creates a Mac application bundle using PyInstaller
"""

import os
import subprocess
import sys
from pathlib import Path

def build_app():
    """Build the Mac application"""
    
    # Ensure we're in the right directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("🔨 Building Who's Your Pokemon Mac Application...")
    
    # PyInstaller command with all necessary options
    cmd = [
        "pyinstaller",
        "--name=Whos Your Pokemon",  # App name
        "--windowed",  # No console window
        "--onedir",  # Create a directory with all files
        "--icon=question_mark.icns",  # Use question mark as app icon
        "--add-data=pokemon_data.json:.",  # Include Pokemon data
        "--add-data=x_icon.png:.",  # Include X icon
        "--add-data=question_mark.icns:.",  # Include app icon
        "--clean",  # Clean cache before building
        "--noconfirm",  # Overwrite without asking
        "main.py"  # Main Python file
    ]
    
    try:
        # Run PyInstaller
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build completed successfully!")
        
        # Print location of built app
        app_path = script_dir / "dist" / "Whos Your Pokemon"
        print(f"📦 Application built at: {app_path}")
        print(f"🚀 To run: open 'dist/Whos Your Pokemon.app'")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with error:")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def create_app_bundle():
    """Create a proper .app bundle for macOS"""
    
    print("📱 Creating Mac .app bundle...")
    
    # Path to the built executable
    dist_path = Path("dist/Whos Your Pokemon")
    app_path = Path("dist/Whos Your Pokemon.app")
    
    if not dist_path.exists():
        print("❌ Built application not found. Run build first.")
        return False
    
    try:
        # Create .app bundle structure
        contents_path = app_path / "Contents"
        macos_path = contents_path / "MacOS"
        resources_path = contents_path / "Resources"
        
        # Create directories
        macos_path.mkdir(parents=True, exist_ok=True)
        resources_path.mkdir(parents=True, exist_ok=True)
        
        # Copy executable and all files
        import shutil
        
        # Copy the entire dist folder contents to MacOS
        if macos_path.exists():
            shutil.rmtree(macos_path)
        shutil.copytree(dist_path, macos_path)
        
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
    <string>question_mark.icns</string>
    <key>CFBundleIdentifier</key>
    <string>com.example.whosyourpokemon</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>Whos Your Pokemon</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.9</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>'''
        
        with open(contents_path / "Info.plist", "w") as f:
            f.write(info_plist)
        
        # Copy icon with standard name for better macOS compatibility
        import shutil
        icon_source = Path("question_mark.icns")
        if icon_source.exists():
            shutil.copy2(icon_source, resources_path / "icon.icns")
            
            # Update Info.plist to use standard icon name
            import subprocess
            subprocess.run([
                "plutil", "-replace", "CFBundleIconFile", "-string", "icon.icns",
                str(contents_path / "Info.plist")
            ], check=True)
        
        # Register with Launch Services to refresh icon
        subprocess.run([
            "/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister",
            "-f", str(app_path)
        ], check=False)  # Don't fail if this doesn't work
        
        print("✅ Mac .app bundle created successfully!")
        print(f"📦 App bundle at: {app_path}")
        print("🚀 Double-click the .app to run!")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create .app bundle: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Who's Your Pokemon - Mac App Builder")
    print("=" * 50)
    
    # Step 1: Build with PyInstaller
    if build_app():
        # Step 2: Create .app bundle
        create_app_bundle()
        
        print("\n" + "=" * 50)
        print("🎉 Build Complete!")
        print("Your app is ready in the 'dist' folder")
        print("=" * 50)
    else:
        print("\n❌ Build failed. Please check the errors above.")
        sys.exit(1)
