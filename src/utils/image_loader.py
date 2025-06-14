"""
Image loading utilities for the Pokemon Guess Game
"""
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from .resource_path import get_resource_path


class ImageLoader:
    """Handles image loading and caching for the game"""
    
    def __init__(self):
        self.image_cache = {}
        self.x_icon = None
        self.image_size = (96, 96)
    
    def load_logo_image(self, filename, max_width=400, max_height=150):
        """Load and resize a logo image while maintaining aspect ratio"""
        try:
            image = Image.open(get_resource_path(f'assets/{filename}'))
            
            # Calculate scaling to fit within max dimensions while maintaining aspect ratio
            original_width, original_height = image.size
            width_ratio = max_width / original_width
            height_ratio = max_height / original_height
            scale_factor = min(width_ratio, height_ratio)
            
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
            
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"❌ Error loading logo {filename}: {e}")
            return None

    def load_x_icon(self):
        """Load and prepare the X icon for elimination overlay"""
        try:
            x_image = Image.open(get_resource_path('assets/x_icon.png'))
            x_image = x_image.resize((96, 96), Image.Resampling.LANCZOS)
            self.x_icon = ImageTk.PhotoImage(x_image)
            print("✅ X icon loaded successfully")
        except Exception as e:
            print(f"❌ Error loading X icon: {e}")
            self.x_icon = None
    
    def download_and_cache_image(self, pokemon_name, sprite_url):
        """Download and cache a Pokémon sprite image"""
        if pokemon_name in self.image_cache:
            return self.image_cache[pokemon_name]
        
        if not sprite_url:
            return None
        
        try:
            response = requests.get(sprite_url, timeout=10)
            response.raise_for_status()
            
            image = Image.open(BytesIO(response.content))
            image = image.resize(self.image_size, Image.Resampling.LANCZOS)
            
            # Convert to RGBA if not already
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            photo = ImageTk.PhotoImage(image)
            self.image_cache[pokemon_name] = photo
            return photo
        except Exception as e:
            print(f"❌ Error loading image for {pokemon_name}: {e}")
            return None
