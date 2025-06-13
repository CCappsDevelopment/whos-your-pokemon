#!/bin/bash
# Convert question_mark.png to .icns format for Mac app icon

echo "🖼️  Converting question_mark.png to app icon..."

# Create iconset directory
mkdir -p question_mark.iconset

# Create different sizes for the iconset
# macOS requires multiple sizes: 16x16, 32x32, 128x128, 256x256, 512x512, 1024x1024
sips -z 16 16 question_mark.png --out question_mark.iconset/icon_16x16.png
sips -z 32 32 question_mark.png --out question_mark.iconset/icon_16x16@2x.png
sips -z 32 32 question_mark.png --out question_mark.iconset/icon_32x32.png
sips -z 64 64 question_mark.png --out question_mark.iconset/icon_32x32@2x.png
sips -z 128 128 question_mark.png --out question_mark.iconset/icon_128x128.png
sips -z 256 256 question_mark.png --out question_mark.iconset/icon_128x128@2x.png
sips -z 256 256 question_mark.png --out question_mark.iconset/icon_256x256.png
sips -z 512 512 question_mark.png --out question_mark.iconset/icon_256x256@2x.png
sips -z 512 512 question_mark.png --out question_mark.iconset/icon_512x512.png
sips -z 1024 1024 question_mark.png --out question_mark.iconset/icon_512x512@2x.png

# Convert iconset to icns
iconutil -c icns question_mark.iconset

# Clean up iconset directory
rm -rf question_mark.iconset

if [ -f "question_mark.icns" ]; then
    echo "✅ Icon converted successfully: question_mark.icns"
else
    echo "❌ Icon conversion failed"
fi
