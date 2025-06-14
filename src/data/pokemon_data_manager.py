"""
Pokemon data management for the Pokemon Guess Game
"""
import json
from ..utils.resource_path import get_resource_path


class PokemonDataManager:
    """Manages Pokemon data loading and filtering"""
    
    def __init__(self):
        self.pokemon_data = self.load_pokemon_data()
        self.pokemon_list = list(self.pokemon_data.keys()) if self.pokemon_data else [
            "Pikachu", "Bulbasaur", "Charmander", "Squirtle", "Caterpie", "Weedle",
            "Pidgey", "Rattata", "Spearow", "Ekans", "Sandshrew", "Nidoran♀",
            "Nidoran♂", "Clefairy", "Vulpix", "Jigglypuff", "Zubat", "Oddish",
            "Paras", "Venonat", "Diglett", "Meowth", "Psyduck", "Mankey"
        ]
    
    def load_pokemon_data(self):
        """Load Pokémon data from the JSON file"""
        try:
            with open(get_resource_path('data_sources/pokemon_data.json'), 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ Loaded {len(data)} Pokémon from data file")
            return data
        except FileNotFoundError:
            print("⚠️  Pokémon data file not found, using fallback list")
            return None
        except Exception as e:
            print(f"❌ Error loading Pokémon data: {e}")
            return None
    
    def get_pokemon_generation(self, pokemon_name):
        """Get the generation information for a Pokémon"""
        if pokemon_name not in self.pokemon_data:
            return "Unknown"
        
        pokemon_info = self.pokemon_data[pokemon_name]
        if isinstance(pokemon_info, dict):
            return pokemon_info.get('generation', 'Unknown')
        else:
            return "Unknown"  # Old format doesn't have generation info
    
    def get_pokemon_sprite_url(self, pokemon_name):
        """Get the sprite URL for a Pokémon"""
        if pokemon_name not in self.pokemon_data:
            return None
        
        pokemon_info = self.pokemon_data[pokemon_name]
        if isinstance(pokemon_info, dict):
            return pokemon_info.get('sprite_url')
        else:
            return pokemon_info  # Old format is just the URL
    
    def filter_pokemon_by_generation(self, selected_generations):
        """Filter Pokémon list based on selected generations"""
        if not self.pokemon_data:
            return []
        
        filtered_list = []
        for pokemon_name, pokemon_info in self.pokemon_data.items():
            if isinstance(pokemon_info, dict):
                generation = pokemon_info.get('generation', '1')
                if generation in selected_generations:
                    filtered_list.append(pokemon_name)
            else:
                # Backward compatibility - include if no generation filtering
                filtered_list.append(pokemon_name)
        
        return filtered_list
