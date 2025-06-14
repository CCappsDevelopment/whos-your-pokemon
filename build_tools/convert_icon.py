#!/usr/bin/env python3
"""
Convert question_mark.png (WebP) to proper icon formats for the app
"""

from PIL import Image
import os
import subprocess

def convert_webp_to_icon():
    """Convert the WebP file to proper icon formats"""
    
    print("🖼️  Converting question_mark.png (WebP) to app icon...")
    
    try:
        # Open the WebP image
        img = Image.open('question_mark.png')
        
        # Convert to RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Save as proper PNG first
        img.save('question_mark_converted.png', 'PNG')
        print("✅ Converted WebP to PNG format")
        
        # Create iconset directory
        os.makedirs('question_mark.iconset', exist_ok=True)
        
        # Create different sizes for the iconset
        sizes = [
            (16, 'icon_16x16.png'),
            (32, 'icon_16x16@2x.png'),
            (32, 'icon_32x32.png'),
            (64, 'icon_32x32@2x.png'),
            (128, 'icon_128x128.png'),
            (256, 'icon_128x128@2x.png'),
            (256, 'icon_256x256.png'),
            (512, 'icon_256x256@2x.png'),
            (512, 'icon_512x512.png'),
            (1024, 'icon_512x512@2x.png')
        ]
        
        for size, filename in sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            resized.save(f'question_mark.iconset/{filename}', 'PNG')
        
        print("✅ Created all icon sizes")
        
        # Convert iconset to icns using iconutil
        result = subprocess.run(['iconutil', '-c', 'icns', 'question_mark.iconset'], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Icon converted successfully: question_mark.icns")
            
            # Clean up
            subprocess.run(['rm', '-rf', 'question_mark.iconset'])
            
            return True
        else:
            print(f"❌ iconutil failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error converting icon: {e}")
        return False

if __name__ == "__main__":
    convert_webp_to_icon()
