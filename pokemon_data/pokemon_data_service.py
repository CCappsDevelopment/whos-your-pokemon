#!/usr/bin/env python3
"""
Pokémon Data Service - Fetches all Pokémon data from PokéAPI
Creates a local data file with names, sprite URLs, and generation info for the game
Only includes Pokémon from the curated list in pokemon_data.json
"""

import requests
import json
import time
from typing import Dict, List, Optional

class PokemonDataService:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2/pokemon"
        self.species_url = "https://pokeapi.co/api/v2/pokemon-species"
        self.pokemon_data = {}
        self.data_file = "pokemon_data.json"
        self.curated_pokemon = self.load_curated_pokemon_list()
    
    def load_curated_pokemon_list(self) -> set:
        """Load the list of curated Pokémon names from the existing pokemon_data.json"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            pokemon_names = set(data.keys())
            print(f"📋 Loaded {len(pokemon_names)} curated Pokémon names")
            return pokemon_names
        except FileNotFoundError:
            print(f"❌ Curated data file {self.data_file} not found, will fetch all Pokémon")
            return set()
        except Exception as e:
            print(f"❌ Error loading curated list: {e}")
            return set()
    
    def get_pokemon_generation(self, poke_id: int) -> Optional[str]:
        """Get the generation information for a Pokémon"""
        try:
            species_url = f"{self.species_url}/{poke_id}/"
            response = requests.get(species_url)
            response.raise_for_status()
            
            species_data = response.json()
            generation_name = species_data["generation"]["name"]
            
            # Convert Roman numerals to numbers
            roman_to_num = {
                "i": "1", "ii": "2", "iii": "3", "iv": "4", "v": "5",
                "vi": "6", "vii": "7", "viii": "8", "ix": "9", "x": "10"
            }
            
            gen_suffix = generation_name.split("-")[-1]
            gen_num = roman_to_num.get(gen_suffix, gen_suffix)
            
            return f"Generation {gen_num}"
            
        except requests.RequestException as e:
            print(f"❌ Error fetching generation for Pokémon ID {poke_id}: {e}")
            return None
        except KeyError as e:
            print(f"❌ Missing generation data for Pokémon ID {poke_id}: {e}")
            return None
    
    def fetch_all_pokemon(self) -> Dict[str, Dict[str, str]]:
        """
        Fetch Pokémon data for curated list with names, sprite URLs, and generation info
        Returns a dictionary with pokemon_name: {sprite_url, generation} pairs
        """
        print("🔄 Starting Pokémon data collection from PokéAPI...")
        
        if not self.curated_pokemon:
            print("❌ No curated Pokémon list found, cannot proceed")
            return {}
        
        # Step 1: Get the full list of all Pokémon to map names to IDs
        print("📋 Fetching complete Pokémon list for ID mapping...")
        try:
            response = requests.get(f"{self.base_url}?limit=100000&offset=0")
            response.raise_for_status()
            pokemon_list = response.json()
            
            # Create name to URL mapping
            name_to_url = {}
            for pokemon in pokemon_list['results']:
                formatted_name = self.format_pokemon_name(pokemon['name'])
                name_to_url[formatted_name] = pokemon['url']
            
            print(f"📊 Found {len(pokemon_list['results'])} total Pokémon in API")
            
        except requests.RequestException as e:
            print(f"❌ Error fetching Pokémon list: {e}")
            return {}
        
        # Step 2: Process only curated Pokémon
        pokemon_data = {}
        processed = 0
        total_curated = len(self.curated_pokemon)
        
        print(f"🎯 Processing {total_curated} curated Pokémon...")
        
        for pokemon_name in self.curated_pokemon:
            try:
                # Show progress every 25 Pokémon
                if processed % 25 == 0:
                    print(f"⏳ Processing {processed}/{total_curated} curated Pokémon...")
                
                # Check if this Pokémon exists in the API
                if pokemon_name not in name_to_url:
                    print(f"⚠️  Pokémon '{pokemon_name}' not found in API, skipping...")
                    processed += 1
                    continue
                
                # Get detailed data for this Pokémon
                details_response = requests.get(name_to_url[pokemon_name])
                details_response.raise_for_status()
                details = details_response.json()
                
                sprite_url = details['sprites']['front_default']
                pokemon_id = details['id']
                
                # Only include Pokémon that have sprites
                if not sprite_url:
                    print(f"⚠️  No sprite for {pokemon_name}, skipping...")
                    processed += 1
                    continue
                
                # Get generation information
                generation = self.get_pokemon_generation(pokemon_id)
                if not generation:
                    generation = "Unknown Generation"
                
                pokemon_data[pokemon_name] = {
                    "sprite_url": sprite_url,
                    "generation": generation
                }
                
                processed += 1
                
                # Be nice to the API - small delay between requests
                time.sleep(0.15)  # Slightly longer delay due to additional API calls
                
            except requests.RequestException as e:
                print(f"❌ Error fetching details for {pokemon_name}: {e}")
                processed += 1
                continue
            except KeyError as e:
                print(f"❌ Missing data field for {pokemon_name}: {e}")
                processed += 1
                continue
        
        print(f"✅ Successfully collected data for {len(pokemon_data)} Pokémon")
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
    
    def save_pokemon_data(self, pokemon_data: Dict[str, Dict[str, str]]) -> bool:
        """Save Pokémon data to a JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(pokemon_data, f, indent=2, ensure_ascii=False)
            print(f"💾 Pokémon data saved to {self.data_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return False
    
    def load_pokemon_data(self) -> Dict[str, Dict[str, str]]:
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
    
    def update_pokemon_data(self) -> Dict[str, Dict[str, str]]:
        """
        Main method to fetch fresh data from API and save it locally
        """
        print("🚀 Starting Pokémon data update process...")
        
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
    
    print("=" * 60)
    print("    POKÉMON DATA COLLECTION SERVICE (WITH GENERATIONS)")
    print("=" * 60)
    print()
    
    if not service.curated_pokemon:
        print("❌ Cannot proceed without curated Pokémon list")
        return {}
    
    print(f"🎯 Target: {len(service.curated_pokemon)} curated Pokémon")
    choice = input("Do you want to fetch generation data for all curated Pokémon? (y/N): ").lower().strip()
    if choice != 'y':
        print("📊 Operation cancelled")
        return {}
    
    # Fetch new data with generation information
    pokemon_data = service.update_pokemon_data()
    
    if pokemon_data:
        print("\n🎮 Sample Pokémon data:")
        sample_items = list(pokemon_data.items())[:5]
        for name, data in sample_items:
            print(f"  {name}:")
            print(f"    Sprite: {data['sprite_url']}")
            print(f"    Generation: {data['generation']}")
        print(f"  ... and {len(pokemon_data) - 5} more Pokémon")
        
        # Show generation distribution
        generation_counts = {}
        for data in pokemon_data.values():
            gen = data['generation']
            generation_counts[gen] = generation_counts.get(gen, 0) + 1
        
        print(f"\n📊 Generation distribution:")
        for gen in sorted(generation_counts.keys()):
            print(f"  {gen}: {generation_counts[gen]} Pokémon")
    
    return pokemon_data

if __name__ == "__main__":
    main()
