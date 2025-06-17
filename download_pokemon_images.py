#!/usr/bin/env python3
"""
Download and cache all Pokemon sprites locally
"""
import json
import os
import requests
from PIL import Image
from io import BytesIO
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Thread-safe counter for progress tracking
class ProgressCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()
    
    def increment(self):
        with self.lock:
            self.count += 1
            return self.count

def download_pokemon_image(pokemon_name, sprite_url, output_dir, progress_counter, total_count):
    """Download a single Pokemon image"""
    try:
        # Create safe filename
        safe_name = pokemon_name.replace('/', '_').replace('\\', '_').replace(':', '_')
        filename = f"{safe_name}.png"
        filepath = os.path.join(output_dir, filename)
        
        # Skip if already exists
        if os.path.exists(filepath):
            current = progress_counter.increment()
            print(f"[{current}/{total_count}] ✅ {pokemon_name} (already cached)")
            return pokemon_name, True, f"assets/pokemon_images/{filename}"
        
        # Download image
        response = requests.get(sprite_url, timeout=15)
        response.raise_for_status()
        
        # Process with PIL to ensure it's valid and resize if needed
        image = Image.open(BytesIO(response.content))
        
        # Resize to 96x96 if not already
        if image.size != (96, 96):
            image = image.resize((96, 96), Image.Resampling.LANCZOS)
        
        # Convert to RGBA for consistency
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Save the image
        image.save(filepath, 'PNG', optimize=True)
        
        current = progress_counter.increment()
        print(f"[{current}/{total_count}] ✅ {pokemon_name}")
        
        return pokemon_name, True, f"assets/pokemon_images/{filename}"
        
    except Exception as e:
        current = progress_counter.increment()
        print(f"[{current}/{total_count}] ❌ {pokemon_name}: {e}")
        return pokemon_name, False, sprite_url

def main():
    print("🚀 Starting Pokemon image download and caching process...")
    
    # Load Pokemon data
    data_file = "data_sources/pokemon_data.json"
    if not os.path.exists(data_file):
        print(f"❌ Pokemon data file not found: {data_file}")
        return
    
    with open(data_file, 'r', encoding='utf-8') as f:
        pokemon_data = json.load(f)
    
    print(f"📊 Found {len(pokemon_data)} Pokemon to process")
    
    # Create output directory
    output_dir = "assets/pokemon_images"
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Created/verified directory: {output_dir}")
    
    # Prepare download tasks
    download_tasks = []
    for pokemon_name, data in pokemon_data.items():
        sprite_url = data.get('sprite_url')
        if sprite_url:
            download_tasks.append((pokemon_name, sprite_url))
    
    total_count = len(download_tasks)
    print(f"🎯 Will download {total_count} images")
    
    # Progress counter
    progress_counter = ProgressCounter()
    
    # Download images in parallel
    results = {}
    failed_downloads = []
    
    start_time = time.time()
    
    # Use ThreadPoolExecutor for parallel downloads
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all download tasks
        future_to_pokemon = {
            executor.submit(download_pokemon_image, pokemon_name, sprite_url, output_dir, progress_counter, total_count): pokemon_name
            for pokemon_name, sprite_url in download_tasks
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_pokemon):
            pokemon_name = future_to_pokemon[future]
            try:
                name, success, path = future.result()
                if success:
                    results[name] = path
                else:
                    failed_downloads.append((name, path))
            except Exception as e:
                print(f"❌ Unexpected error for {pokemon_name}: {e}")
                failed_downloads.append((pokemon_name, str(e)))
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n🎉 Download process completed in {duration:.2f} seconds")
    print(f"✅ Successfully downloaded: {len(results)}")
    print(f"❌ Failed downloads: {len(failed_downloads)}")
    
    if failed_downloads:
        print("\n📋 Failed downloads:")
        for name, error in failed_downloads[:10]:  # Show first 10
            print(f"  - {name}: {error}")
        if len(failed_downloads) > 10:
            print(f"  ... and {len(failed_downloads) - 10} more")
    
    # Update Pokemon data with local paths
    print("\n📝 Updating pokemon_data.json with local image paths...")
    updated_count = 0
    
    for pokemon_name in pokemon_data:
        if pokemon_name in results:
            pokemon_data[pokemon_name]['sprite_url'] = results[pokemon_name]
            pokemon_data[pokemon_name]['local_image'] = True
            updated_count += 1
        else:
            # Mark as remote image for fallback
            pokemon_data[pokemon_name]['local_image'] = False
    
    # Save updated data
    backup_file = "data_sources/pokemon_data_backup_before_local_images.json"
    print(f"💾 Creating backup: {backup_file}")
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(pokemon_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saving updated pokemon_data.json...")
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(pokemon_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Updated {updated_count} Pokemon entries with local image paths")
    print(f"📊 Final stats:")
    print(f"  - Total Pokemon: {len(pokemon_data)}")
    print(f"  - Local images: {len(results)}")
    print(f"  - Remote fallbacks: {len(failed_downloads)}")
    print(f"  - Processing time: {duration:.2f}s")
    print(f"  - Average per image: {(duration/total_count):.3f}s")
    
    print("\n🎯 Next steps:")
    print("1. Update image_loader.py to prioritize local images")
    print("2. Test the application with faster image loading")
    
if __name__ == "__main__":
    main()
