#!/bin/bash
# Linux build script for Who's Your Pokemon
# Run this script on a Linux machine

echo "============================================================"
echo "Who's Your Pokemon - Linux Builder"
echo "============================================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.7+ first."
    exit 1
fi

# Install required packages
echo "📦 Installing required packages..."
pip3 install pyinstaller pillow requests

# Check if required files exist
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found. Please run this from the project root directory."
    exit 1
fi

echo "🔨 Building Who's Your Pokemon for Linux..."

# Run PyInstaller with Linux-specific settings
pyinstaller \
    --name="Whos Your Pokemon" \
    --windowed \
    --onedir \
    --add-data="data_sources/pokemon_data.json:data_sources" \
    --add-data="assets:assets" \
    --clean \
    --noconfirm \
    main.py

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo "✅ Build completed successfully!"
echo "📦 Application built at: dist/Whos Your Pokemon"
echo "🚀 To run: ./dist/Whos Your Pokemon/Whos Your Pokemon"

# Create a simple launcher script
echo "📎 Creating launcher..."
cat > "dist/Whos Your Pokemon/run_game.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
./Whos\ Your\ Pokemon
EOF

chmod +x "dist/Whos Your Pokemon/run_game.sh"
echo "✅ Created launcher: run_game.sh"

echo ""
echo "============================================================"
echo "🎉 Linux Build Complete!"
echo "Your app is ready in the 'dist' folder"
echo "============================================================"
