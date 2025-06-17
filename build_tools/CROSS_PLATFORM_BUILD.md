# Cross-Platform Build Instructions

This document provides detailed instructions for building "Who's Your Pokémon" on different operating systems.

## Prerequisites

### All Platforms
- Python 3.7 or higher
- pip (Python package installer)
- Internet connection (for downloading dependencies)

### Platform-Specific Requirements

#### macOS
- Xcode Command Line Tools (install with: `xcode-select --install`)
- PyInstaller, Pillow, requests

#### Windows
- Windows 10 or higher
- PyInstaller, Pillow, requests
- Optional: NSIS for creating installers

#### Linux
- Python 3.7+
- tkinter development libraries: `sudo apt-get install python3-tk` (Ubuntu/Debian)
- PyInstaller, Pillow, requests

## Quick Build Instructions

### macOS
```bash
# Run from project root directory
python3 build_tools/build_app.py
```

### Windows
```cmd
REM Run from project root directory
build_tools\build_windows.bat
```

### Linux
```bash
# Run from project root directory
chmod +x build_tools/build_linux.sh
./build_tools/build_linux.sh
```

## Detailed Build Process

### 1. Environment Setup

#### macOS/Linux
```bash
# Navigate to project directory
cd /path/to/whos-your-pokemon

# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

#### Windows
```cmd
REM Navigate to project directory
cd C:\path\to\whos-your-pokemon

REM Create virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt
```

### 2. Prepare Assets

Make sure all assets are ready:
```bash
# Download Pokemon data and images (run once)
python3 data_sources/pokemon_data_service.py
```

This will:
- Download complete Pokemon database
- Cache all 1,280+ Pokemon images locally
- Ensure optimal performance

### 3. Build Application

#### Manual PyInstaller Command (Advanced)

##### macOS
```bash
pyinstaller \
    --name="Whos Your Pokemon" \
    --windowed \
    --onedir \
    --icon=assets/question_mark.icns \
    --add-data="data_sources/pokemon_data.json:data_sources" \
    --add-data="assets:assets" \
    --clean \
    --noconfirm \
    main.py
```

##### Windows
```cmd
pyinstaller ^
    --name="Whos Your Pokemon" ^
    --windowed ^
    --onedir ^
    --icon=assets/question_mark.ico ^
    --add-data="data_sources/pokemon_data.json;data_sources" ^
    --add-data="assets;assets" ^
    --clean ^
    --noconfirm ^
    main.py
```

##### Linux
```bash
pyinstaller \
    --name="Whos Your Pokemon" \
    --windowed \
    --onedir \
    --add-data="data_sources/pokemon_data.json:data_sources" \
    --add-data="assets:assets" \
    --clean \
    --noconfirm \
    main.py
```

## Build Output

### macOS
- **Executable Bundle**: `dist/Whos Your Pokemon.app`
- **Directory Bundle**: `dist/Whos Your Pokemon/`
- **Size**: ~99MB (includes all Pokemon images)
- **Distribution**: Copy `.app` file to other Macs

### Windows
- **Executable**: `dist/Whos Your Pokemon/Whos Your Pokemon.exe`
- **Launcher**: `dist/Whos Your Pokemon/Run Game.bat`
- **Size**: ~95MB (includes all Pokemon images)
- **Distribution**: Copy entire `Whos Your Pokemon` folder

### Linux
- **Executable**: `dist/Whos Your Pokemon/Whos Your Pokemon`
- **Launcher**: `dist/Whos Your Pokemon/run_game.sh`
- **Size**: ~90MB (includes all Pokemon images)
- **Distribution**: Copy entire `Whos Your Pokemon` folder

## Troubleshooting

### Common Issues

#### "Module not found" errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're using the correct Python environment

#### Missing Pokemon images
- Run the data service: `python3 data_sources/pokemon_data_service.py`
- Ensure internet connection during first setup

#### Icon not displaying (Windows)
- The build script automatically creates a `.ico` file from the PNG
- If issues persist, ensure Pillow is installed: `pip install pillow`

#### Permission denied (Linux/macOS)
- Make build scripts executable: `chmod +x build_tools/build_linux.sh`
- Run with appropriate permissions

### Platform-Specific Issues

#### macOS
- **Gatekeeper warnings**: Right-click → Open, then "Open" to bypass security
- **Notarization**: For distribution, apps need to be notarized by Apple

#### Windows
- **Antivirus false positives**: PyInstaller executables sometimes trigger warnings
- **Missing DLLs**: Usually resolved by including all dependencies in the build

#### Linux
- **Missing system libraries**: Install tkinter dev packages: `sudo apt-get install python3-tk`
- **Display issues**: Ensure X11 is running for GUI applications

## Cross-Compilation Notes

### Building for Other Platforms

PyInstaller generally requires building on the target platform:
- **Windows builds**: Must be built on Windows
- **macOS builds**: Must be built on macOS  
- **Linux builds**: Must be built on Linux

### Alternative: Docker Builds

For automated cross-platform builds, consider using Docker with platform-specific containers.

## Distribution

### File Sharing
- **macOS**: Share the `.app` file
- **Windows**: ZIP the entire `Whos Your Pokemon` folder
- **Linux**: TAR/ZIP the entire `Whos Your Pokemon` folder

### Size Optimization
Current builds include all Pokemon images (~50MB) for offline use. To reduce size:
1. Remove images from `assets/pokemon_images/`
2. Images will download on-demand (requires internet)
3. Rebuild application

## Version Information

- **Build Scripts Version**: 2.0
- **Application Version**: 2.0
- **Supported Platforms**: macOS 10.14+, Windows 10+, Linux (Ubuntu 18.04+)
- **Python Version**: 3.7+
