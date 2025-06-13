# Building Who's Your Pokemon for Mac

## Quick Build Instructions

### Option 1: Use the Build Script (Recommended)
```bash
./build.sh
```

### Option 2: Manual PyInstaller Command
```bash
source .venv/bin/activate

pyinstaller \
  --name="Whos Your Pokemon" \
  --windowed \
  --onedir \
  --icon="question_mark.icns" \
  --add-data="pokemon_data.json:." \
  --add-data="x_icon.png:." \
  --clean \
  --noconfirm \
  main.py
```

## What Gets Built

After building, you'll find in the `dist/` folder:

1. **`Whos Your Pokemon.app`** - Double-clickable Mac application
2. **`Whos Your Pokemon/`** - Directory with executable and all dependencies

## How to Run the Built Application

### Method 1: Mac .app Bundle (Easiest)
- Double-click `dist/Whos Your Pokemon.app`
- Or from Terminal: `open "dist/Whos Your Pokemon.app"`

### Method 2: Direct Executable
```bash
cd "dist/Whos Your Pokemon"
./Whos\ Your\ Pokemon
```

## Distribution

### To share your app with others:

1. **For casual sharing**: Zip the `Whos Your Pokemon.app` file
2. **For complete portability**: Zip the entire `Whos Your Pokemon/` folder

### Requirements for other Macs:
- macOS 10.9 or later
- No Python installation needed (everything is bundled!)

## File Structure

```
dist/
├── Whos Your Pokemon.app/          # Mac application bundle
│   └── Contents/
│       ├── Info.plist             # App metadata
│       ├── MacOS/                 # Executable and dependencies
│       └── Resources/             # App resources (includes question_mark.icns)
└── Whos Your Pokemon/              # Standalone directory
    ├── Whos Your Pokemon          # Main executable
    ├── _internal/                 # Python runtime and libraries
    ├── pokemon_data.json          # Pokemon data
    └── x_icon.png                 # X icon for eliminated Pokemon
```

## Troubleshooting

### If the app won't run:
1. **Security Warning**: Right-click the .app → "Open" → "Open" to bypass Gatekeeper
2. **Missing Data**: Ensure `pokemon_data.json` and `x_icon.png` are in the same folder as the executable

### To rebuild:
```bash
# Clean previous builds
rm -rf build dist *.spec

# Run build again
./build.sh
```

## Build Requirements

- Python 3.11+
- Virtual environment with dependencies:
  - pillow>=10.0.0
  - requests>=2.25.0
  - pyinstaller>=5.0.0

## Advanced Options

### Create a single file executable:
```bash
pyinstaller --onefile --windowed main.py
```
(Note: Slower startup but single file)

### Add custom icon:
```bash
pyinstaller --icon=question_mark.icns main.py
```
(Using the question mark icon for the app)

### Debug mode (shows console):
```bash
pyinstaller --debug=all main.py
```

## Notes

- The built app includes the entire Python runtime (~50-100 MB)
- First startup may be slower as the app extracts dependencies
- The app is portable - copy the folder/app to any Mac to run
- Pokemon data is fetched from the internet, so internet connection is required for first-time Pokemon loading
