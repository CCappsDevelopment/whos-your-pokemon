#!/usr/bin/env python3
"""
Pokémon Data Service - Fetches all Pokémon data from PokéAPI
Creates a local data file with names and sprite URLs for the game
"""

import requests
import json
import time
from typing import Dict, List

class PokemonDataService:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2/pokemon"
        self.pokemon_data = {}
        self.data_file = "pokemon_data.json"
    
    def fetch_all_pokemon(self) -> Dict[str, str]:
        """
        Fetch all Pokémon names and their front sprite URLs from PokéAPI
        Returns a dictionary with pokemon_name: sprite_url pairs
        """
        print("🔄 Starting Pokémon data collection from PokéAPI...")
        
        # Step 1: Get the list of all Pokémon
        print("📋 Fetching Pokémon list...")
        try:
            response = requests.get(f"{self.base_url}?limit=100000&offset=0")
            response.raise_for_status()
            pokemon_list = response.json()
            
            total_pokemon = len(pokemon_list['results'])
            print(f"📊 Found {total_pokemon} Pokémon to process")
            
        except requests.RequestException as e:
            print(f"❌ Error fetching Pokémon list: {e}")
            return {}
        
        # Step 2: Fetch details for each Pokémon
        pokemon_data = {}
        processed = 0
        
        for pokemon in pokemon_list['results']:
            try:
                # Show progress every 50 Pokémon
                if processed % 50 == 0:
                    print(f"⏳ Processing {processed}/{total_pokemon} Pokémon...")
                
                # Get detailed data for this Pokémon
                details_response = requests.get(pokemon['url'])
                details_response.raise_for_status()
                details = details_response.json()
                
                name = details['name'].title()  # Capitalize first letter
                sprite_url = details['sprites']['front_default']
                
                # Only include Pokémon that have sprites
                if sprite_url:
                    pokemon_data[name] = sprite_url
                else:
                    print(f"⚠️  No sprite for {name}, skipping...")
                
                processed += 1
                
                # Be nice to the API - small delay between requests
                time.sleep(0.1)
                
            except requests.RequestException as e:
                print(f"❌ Error fetching details for {pokemon['name']}: {e}")
                continue
            except KeyError as e:
                print(f"❌ Missing data field for {pokemon['name']}: {e}")
                continue
        
        print(f"✅ Successfully collected data for {len(pokemon_data)} Pokémon")
        return pokemon_data
    
    def save_pokemon_data(self, pokemon_data: Dict[str, str]) -> bool:
        """Save Pokémon data to a JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(pokemon_data, f, indent=2, ensure_ascii=False)
            print(f"💾 Pokémon data saved to {self.data_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return False
    
    def load_pokemon_data(self) -> Dict[str, str]:
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
    
    def update_pokemon_data(self) -> Dict[str, str]:
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
    
    print("=" * 50)
    print("    POKÉMON DATA COLLECTION SERVICE")
    print("=" * 50)
    print()
    
    # Check if data file already exists
    try:
        existing_data = service.load_pokemon_data()
        if existing_data:
            print(f"📋 Found existing data file with {len(existing_data)} Pokémon")
            choice = input("Do you want to update the data? (y/N): ").lower().strip()
            if choice != 'y':
                print("📊 Using existing data")
                return existing_data
    except:
        pass
    
    # Fetch new data
    pokemon_data = service.update_pokemon_data()
    
    if pokemon_data:
        print("\n🎮 Sample Pokémon data:")
        sample_items = list(pokemon_data.items())[:5]
        for name, url in sample_items:
            print(f"  {name}: {url}")
        print(f"  ... and {len(pokemon_data) - 5} more Pokémon")
    
    return pokemon_data

if __name__ == "__main__":
    main()
