#!/bin/bash
# Simple build script for Who's Your Pokemon

echo "🔨 Building Who's Your Pokemon Mac Application..."

# Activate virtual environment and build
source .venv/bin/activate

# Clean previous builds
rm -rf build dist *.spec

# Build the application
pyinstaller \
  --name="Whos Your Pokemon" \
  --windowed \
  --onedir \
  --add-data="pokemon_data.json:." \
  --add-data="x_icon.png:." \
  --clean \
  --noconfirm \
  main.py

echo ""
if [ -d "dist/Whos Your Pokemon" ]; then
    echo "✅ Build completed successfully!"
    echo "📦 Application built at: dist/Whos Your Pokemon/"
    echo "🚀 To run the app:"
    echo "   cd 'dist/Whos Your Pokemon'"
    echo "   ./Whos Your Pokemon"
    echo ""
    echo "📁 All files needed to run are in the 'dist/Whos Your Pokemon' folder"
    echo "   You can copy this entire folder to another Mac to run the game"
else
    echo "❌ Build failed!"
fi
