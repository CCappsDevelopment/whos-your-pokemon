"""
Image loading utilities for the Pokemon Guess Game
"""
import tkinter as tk
from PIL import Image, ImageTk, ImageFile
import requests
from io import BytesIO
import os
from .resource_path import get_resource_path

# Enable loading of truncated images to handle potentially problematic PNG files
ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageLoader:
    """Handles image loading and caching for the game"""
    
    def __init__(self):
        self.image_cache = {}
        self.x_icon = None
        self.image_size = (96, 96)
        self.autocomplete_size = (64, 64)
    
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
    
    def load_pokemon_image(self, pokemon_name, sprite_url):
        """Load a Pokémon sprite image (96x96), prioritizing local cache over remote downloads"""
        if pokemon_name in self.image_cache:
            return self.image_cache[pokemon_name]
        
        # First, try to load from local cache
        local_image = self._load_local_image_sized(pokemon_name, self.image_size)
        if local_image:
            self.image_cache[pokemon_name] = local_image
            return local_image
        
        # If local image not available, download from URL
        if sprite_url:
            downloaded_image = self._download_image_from_url_sized(pokemon_name, sprite_url, self.image_size)
            if downloaded_image:
                self.image_cache[pokemon_name] = downloaded_image
                return downloaded_image
        
        print(f"❌ Failed to load image for {pokemon_name}")
        return None
    
    def load_pokemon_image_autocomplete(self, pokemon_name, sprite_url):
        """Load a Pokémon sprite image for autocomplete (64x64), prioritizing local cache"""
        cache_key = f"{pokemon_name}_autocomplete"
        
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
        
        # First, try to load from local cache
        local_image = self._load_local_image_sized(pokemon_name, self.autocomplete_size)
        if local_image:
            self.image_cache[cache_key] = local_image
            return local_image
        
        # If local image not available, download from URL
        if sprite_url:
            downloaded_image = self._download_image_from_url_sized(pokemon_name, sprite_url, self.autocomplete_size)
            if downloaded_image:
                self.image_cache[cache_key] = downloaded_image
                return downloaded_image
        
        print(f"❌ Failed to load autocomplete image for {pokemon_name}")
        return None
    
    def _load_local_image_sized(self, pokemon_name, size):
        """Load a Pokémon image from local assets folder with specific size"""
        try:
            # Try different possible filenames
            possible_names = [
                pokemon_name.lower().replace(' ', '_').replace('.', '').replace("'", ''),
                pokemon_name.lower().replace(' ', '-').replace('.', '').replace("'", ''),
                pokemon_name.lower()
            ]
            
            for name in possible_names:
                local_path = get_resource_path(f'assets/pokemon_images/{name}.png')
                if os.path.exists(local_path):
                    image = Image.open(local_path)
                    image = image.resize(size, Image.Resampling.LANCZOS)
                    
                    # Convert to RGBA if not already
                    if image.mode != 'RGBA':
                        image = image.convert('RGBA')
                    
                    return ImageTk.PhotoImage(image)
            
            return None
        except Exception as e:
            print(f"❌ Error loading local image for {pokemon_name}: {e}")
            return None
    
    def _download_image_from_url_sized(self, pokemon_name, sprite_url, size):
        """Download a Pokémon sprite image from remote URL with specific size as fallback"""
        try:
            print(f"📥 Downloading image for {pokemon_name} from remote URL...")
            response = requests.get(sprite_url, timeout=10)
            response.raise_for_status()
            
            # Try multiple approaches to handle potentially problematic images
            image = None
            
            # Approach 1: Standard BytesIO method
            try:
                bio = BytesIO(response.content)
                bio.seek(0)
                image = Image.open(bio)
            except Exception as e1:
                # Approach 2: Try to save to temp file and load
                try:
                    import tempfile
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                        tmp.write(response.content)
                        tmp_path = tmp.name
                    
                    image = Image.open(tmp_path)
                    os.unlink(tmp_path)  # Clean up
                    print(f"⚠️ Used fallback method for {pokemon_name}")
                except Exception as e2:
                    # Approach 3: Try with PIL's load_truncated_images option
                    try:
                        ImageFile.LOAD_TRUNCATED_IMAGES = True
                        bio = BytesIO(response.content)
                        bio.seek(0)
                        image = Image.open(bio)
                        print(f"⚠️ Used truncated image loading for {pokemon_name}")
                    except Exception as e3:
                        print(f"❌ All methods failed for {pokemon_name}: {e3}")
                        return None
            
            if image:
                # Process the image with specified size
                image = image.resize(size, Image.Resampling.LANCZOS)
                
                # Convert to RGBA if not already
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')
                
                return ImageTk.PhotoImage(image)
            
        except Exception as e:
            print(f"❌ Error downloading image for {pokemon_name}: {e}")
            return None
