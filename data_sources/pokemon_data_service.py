#!/usr/bin/env python3
"""
Pokémon Data Service - Fetches ALL Pokémon data from PokéAPI
Creates a local data file with names, sprite URLs, generation info, and variant classifications
Now includes ALL Pokémon from the PokéAPI with proper variant categorization
"""

import requests
import json
import time
import re
from typing import Dict, List, Optional

class PokemonDataService:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2/pokemon"
        self.species_url = "https://pokeapi.co/api/v2/pokemon-species"
        self.pokemon_data = {}
        self.data_file = "pokemon_data.json"
        self.variant_patterns = {
            "Regional - Alolan": ["alolan", "alola"],
            "Regional - Galarian": ["galarian", "galar"],
            "Regional - Hisuian": ["hisuian", "hisui"],
            "Regional - Paldean": ["paldean", "paldea"],
            "Gigantamax": ["gigantamax", "gmax"],
            "Mega": ["mega"],
            "Special Pikachus": ["pikachu-cosplay", "pikachu-rock-star", "pikachu-belle", 
                               "pikachu-pop-star", "pikachu-phd", "pikachu-libre", 
                               "pikachu-original-cap", "pikachu-hoenn-cap", "pikachu-sinnoh-cap",
                               "pikachu-unova-cap", "pikachu-kalos-cap", "pikachu-alola-cap",
                               "pikachu-partner-cap", "pikachu-world-cap"],
            "Totem Pokemon": ["totem"],
            "Paradox Pokemon": ["walking-wake", "iron-leaves", "roaring-moon", "iron-valiant",
                              "flutter-mane", "slither-wing", "sandy-shocks", "scream-tail",
                              "brute-bonnet", "iron-treads", "iron-moth", "iron-hands",
                              "iron-jugulis", "iron-thorns", "iron-bundle", "iron-crown",
                              "iron-boulder", "gouging-fire", "raging-bolt"]
        }
    
    def classify_variant(self, pokemon_name: str) -> Optional[str]:
        """Classify a Pokémon as a variant based on its name"""
        name_lower = pokemon_name.lower()
        
        for variant_type, patterns in self.variant_patterns.items():
            for pattern in patterns:
                if pattern in name_lower:
                    return variant_type
        
        # Additional variant detection for forms and other patterns
        if any(form in name_lower for form in ["-altered", "-origin", "-sky", "-land", "-attack", "-defense", "-speed"]):
            return "Form Variants"
        if any(size in name_lower for size in ["-small", "-large", "-super", "-average"]):
            return "Size Variants"
        
        return None
    
    def get_best_sprite_url(self, sprites_data: dict) -> Optional[str]:
        """Get the best available sprite URL from the sprites data"""
        # Try front_default first
        if sprites_data.get('front_default'):
            return sprites_data['front_default']
        
        # Check other front sprites
        front_options = ['front_shiny', 'front_female', 'front_shiny_female']
        for option in front_options:
            if sprites_data.get(option):
                return sprites_data[option]
        
        # Check versions object for more sprite options
        if 'versions' in sprites_data:
            for generation, version_data in sprites_data['versions'].items():
                for game, game_sprites in version_data.items():
                    if isinstance(game_sprites, dict):
                        for sprite_key, sprite_url in game_sprites.items():
                            if sprite_url and 'front' in sprite_key:
                                return sprite_url
        
        # Check other object for additional sprites
        if 'other' in sprites_data:
            for sprite_set, sprite_data in sprites_data['other'].items():
                if isinstance(sprite_data, dict):
                    if sprite_data.get('front_default'):
                        return sprite_data['front_default']
                    # Try other front options in this set
                    for key, url in sprite_data.items():
                        if url and 'front' in key:
                            return url
        
        return None
    
    def get_pokemon_generation(self, poke_id: int) -> int:
        """Get the generation number for a Pokémon"""
        try:
            species_url = f"{self.species_url}/{poke_id}/"
            response = requests.get(species_url)
            response.raise_for_status()
            
            species_data = response.json()
            generation_name = species_data["generation"]["name"]
            
            # Convert Roman numerals to numbers
            roman_to_num = {
                "generation-i": 1, "generation-ii": 2, "generation-iii": 3, 
                "generation-iv": 4, "generation-v": 5, "generation-vi": 6, 
                "generation-vii": 7, "generation-viii": 8, "generation-ix": 9
            }
            
            return roman_to_num.get(generation_name, -1)
            
        except requests.RequestException as e:
            print(f"❌ Error fetching generation for Pokémon ID {poke_id}: {e}")
            return -1
        except KeyError as e:
            print(f"❌ Missing generation data for Pokémon ID {poke_id}: {e}")
            return -1
    
    def fetch_all_pokemon(self) -> Dict[str, Dict]:
        """
        Fetch ALL Pokémon data from PokéAPI with names, sprite URLs, generation info, and variant classification
        Returns a dictionary with pokemon_name: {sprite_url, generation, variant} pairs
        """
        print("🔄 Starting complete Pokémon data collection from PokéAPI...")
        
        # Step 1: Get the complete list of all Pokémon
        print("📋 Fetching complete Pokémon list from PokéAPI...")
        try:
            response = requests.get(f"{self.base_url}?limit=100000&offset=0")
            response.raise_for_status()
            pokemon_list = response.json()
            
            total_pokemon = len(pokemon_list['results'])
            print(f"📊 Found {total_pokemon} total Pokémon in API")
            
        except requests.RequestException as e:
            print(f"❌ Error fetching Pokémon list: {e}")
            return {}
        
        # Step 2: Process all Pokémon
        pokemon_data = {}
        processed = 0
        
        print(f"🎯 Processing all {total_pokemon} Pokémon...")
        
        for pokemon in pokemon_list['results']:
            try:
                # Show progress every 100 Pokémon
                if processed % 100 == 0:
                    print(f"⏳ Processing {processed}/{total_pokemon} Pokémon...")
                
                # Get detailed data for this Pokémon
                details_response = requests.get(pokemon['url'])
                details_response.raise_for_status()
                details = details_response.json()
                
                pokemon_name = self.format_pokemon_name(pokemon['name'])
                pokemon_id = details['id']
                
                # Get the best available sprite
                sprite_url = self.get_best_sprite_url(details['sprites'])
                
                # Skip Pokémon without any sprites
                if not sprite_url:
                    print(f"⚠️  No sprite for {pokemon_name}, skipping...")
                    processed += 1
                    continue
                
                # Get generation information
                generation = self.get_pokemon_generation(pokemon_id)
                
                # Classify variant
                variant = self.classify_variant(pokemon_name)
                
                pokemon_data[pokemon_name] = {
                    "sprite_url": sprite_url,
                    "generation": generation,
                    "variant": variant
                }
                
                processed += 1
                
                # Be nice to the API - small delay between requests
                time.sleep(0.1)
                
            except requests.RequestException as e:
                print(f"❌ Error fetching details for {pokemon['name']}: {e}")
                processed += 1
                continue
            except KeyError as e:
                print(f"❌ Missing data field for {pokemon['name']}: {e}")
                processed += 1
                continue
        
        print(f"✅ Successfully collected data for {len(pokemon_data)} Pokémon")
        
        # Show variant distribution
        variant_counts = {}
        for data in pokemon_data.values():
            variant = data['variant'] or 'Standard'
            variant_counts[variant] = variant_counts.get(variant, 0) + 1
        
        print(f"\n📊 Variant distribution:")
        for variant in sorted(variant_counts.keys()):
            print(f"  {variant}: {variant_counts[variant]} Pokémon")
        
        return pokemon_data
    
    def format_pokemon_name(self, api_name: str) -> str:
        """Convert API name format to our curated format"""
        # Handle special cases for formatting
        name = api_name.replace('-', '-')  # Keep hyphens as-is for regional variants
        
        # Convert to title case but handle special cases
        parts = name.split('-')
        formatted_parts = []
        
        for part in parts:
            if part.lower() in ['jr', 'mr', 'mime']:
                formatted_parts.append(part.title())
            else:
                formatted_parts.append(part.capitalize())
        
        return '-'.join(formatted_parts)
    
    def save_pokemon_data(self, pokemon_data: Dict[str, Dict]) -> bool:
        """Save Pokémon data to a JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(pokemon_data, f, indent=2, ensure_ascii=False)
            print(f"💾 Pokémon data saved to {self.data_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return False
    
    def load_pokemon_data(self) -> Dict[str, Dict]:
        """Load Pokémon data from the JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"📂 Loaded data for {len(data)} Pokémon from {self.data_file}")
            return data
        except FileNotFoundError:
            print(f"❌ Data file {self.data_file} not found")
            return {}
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return {}
    
    def update_pokemon_data(self) -> Dict[str, Dict]:
        """
        Main method to fetch fresh data from API and save it locally
        """
        print("🚀 Starting complete Pokémon data update process...")
        
        pokemon_data = self.fetch_all_pokemon()
        
        if pokemon_data:
            if self.save_pokemon_data(pokemon_data):
                print("🎉 Pokémon data update completed successfully!")
                return pokemon_data
            else:
                print("❌ Failed to save Pokémon data")
        else:
            print("❌ No Pokémon data was collected")
        
        return {}

def main():
    """Main function to run the data collection"""
    service = PokemonDataService()
    
    print("=" * 70)
    print("    COMPLETE POKÉMON DATA COLLECTION SERVICE (WITH VARIANTS)")
    print("=" * 70)
    print()
    
    print("🎯 Target: ALL Pokémon from PokéAPI with variant classification")
    choice = input("Do you want to fetch complete Pokémon data with variants? (y/N): ").lower().strip()
    if choice != 'y':
        print("📊 Operation cancelled")
        return {}
    
    # Fetch new data with generation and variant information
    pokemon_data = service.update_pokemon_data()
    
    if pokemon_data:
        print("\n🎮 Sample Pokémon data:")
        sample_items = list(pokemon_data.items())[:5]
        for name, data in sample_items:
            print(f"  {name}:")
            print(f"    Sprite: {data['sprite_url']}")
            print(f"    Generation: {data['generation']}")
            print(f"    Variant: {data['variant'] or 'Standard'}")
        print(f"  ... and {len(pokemon_data) - 5} more Pokémon")
        
        # Show generation distribution
        generation_counts = {}
        for data in pokemon_data.values():
            gen = data['generation']
            if gen == -1:
                gen_label = "Unknown"
            else:
                gen_label = f"Generation {gen}"
            generation_counts[gen_label] = generation_counts.get(gen_label, 0) + 1
        
        print(f"\n📊 Generation distribution:")
        for gen in sorted(generation_counts.keys()):
            print(f"  {gen}: {generation_counts[gen]} Pokémon")
    
    return pokemon_data

if __name__ == "__main__":
    main()
