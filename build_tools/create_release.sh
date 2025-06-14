#!/bin/bash
# Create distribution package for Who's Your Pokemon

echo "📦 Creating distribution package..."

# Create distribution folder
mkdir -p "release"

# Copy the .app bundle
cp -R "dist/Whos Your Pokemon.app" "release/"

# Create a README for users
cat > "release/README.txt" << EOF
Who's Your Pokemon - Mac Game

INSTALLATION:
1. Double-click "Whos Your Pokemon.app" to run the game
2. If you get a security warning, right-click the app and select "Open"

REQUIREMENTS:
- macOS 10.9 or later
- Internet connection (for downloading Pokemon images)

GAMEPLAY:
- Each player chooses a Pokemon
- Take turns asking questions to eliminate Pokemon
- First to guess the opponent's Pokemon wins!

Enjoy the game!
EOF

# Create zip file
cd release
zip -r "../Whos Your Pokemon - Mac.zip" .
cd ..

echo "✅ Distribution package created: 'Whos Your Pokemon - Mac.zip'"
echo "📤 Ready to share with others!"

# Show file size
echo "📊 Package size: $(du -h "Whos Your Pokemon - Mac.zip" | cut -f1)"
