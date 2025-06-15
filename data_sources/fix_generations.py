#!/usr/bin/env python3
"""
Fix Pokemon generations for variant Pokemon in pokemon_data.json
Replace generation -1 with correct generation based on base Pokemon
"""

import json
import re

def get_base_pokemon_name(variant_name):
    """Extract the base Pokemon name from a variant name"""
    # Common patterns for variants
    patterns = [
        r'^([A-Za-z]+)-.*$',  # Most variants: "Pokemon-Something"
        r'^([A-Za-z]+)$',      # Base form
    ]
    
    for pattern in patterns:
        match = re.match(pattern, variant_name)
        if match:
            return match.group(1)
    
    return variant_name

def load_generation_mappings():
    """Create a mapping of base Pokemon names to their generations"""
    return {
        # Generation 1
        'Venusaur': 1, 'Charizard': 1, 'Blastoise': 1, 'Alakazam': 1, 'Slowbro': 1,
        'Gengar': 1, 'Kangaskhan': 1, 'Pinsir': 1, 'Gyarados': 1, 'Aerodactyl': 1,
        'Mewtwo': 1, 'Mew': 1, 'Pikachu': 1,
        
        # Generation 2
        'Ampharos': 2, 'Steelix': 2, 'Scizor': 2, 'Heracross': 2, 'Houndoom': 2,
        'Tyranitar': 2,
        
        # Generation 3
        'Sceptile': 3, 'Blaziken': 3, 'Swampert': 3, 'Gardevoir': 3, 'Sableye': 3,
        'Mawile': 3, 'Aggron': 3, 'Medicham': 3, 'Manectric': 3, 'Sharpedo': 3,
        'Camerupt': 3, 'Altaria': 3, 'Banette': 3, 'Absol': 3, 'Glalie': 3,
        'Salamence': 3, 'Metagross': 3, 'Latias': 3, 'Latios': 3, 'Rayquaza': 3,
        'Groudon': 3, 'Kyogre': 3, 'Deoxys': 3,
        
        # Generation 4
        'Dialga': 4, 'Palkia': 4, 'Giratina': 4, 'Shaymin': 4, 'Arceus': 4,
        'Rotom': 4, 'Garchomp': 4, 'Lucario': 4, 'Abomasnow': 4,
        
        # Generation 5
        'Audino': 5, 'Reshiram': 5, 'Zekrom': 5, 'Kyurem': 5, 'Keldeo': 5,
        'Meloetta': 5, 'Genesect': 5,
        
        # Generation 6
        'Diancie': 6, 'Hoopa': 6, 'Volcanion': 6, 'Pumpkaboo': 6, 'Gourgeist': 6,
        
        # Generation 7
        'Oricorio': 7, 'Lycanroc': 7, 'Wishiwashi': 7, 'Minior': 7, 'Mimikyu': 7,
        'Necrozma': 7, 'Magearna': 7, 'Marshadow': 7, 'Zeraora': 7,
        'Toxapex': 7, 'Mudsdale': 7, 'Kommo': 7,
        
        # Generation 8
        'Morpeko': 8, 'Eiscue': 8, 'Indeedee': 8, 'Urshifu': 8, 'Calyrex': 8,
        'Toxapex': 7,  # Correcting this
        'Cramorant': 8, 'Enamorus': 8,
        
        # Generation 9
        'Gimmighoul': 9, 'Palafin': 9, 'Tatsugiri': 9, 'Dudunsparce': 9,
        'Squawkabilly': 9, 'Annihilape': 9, 'Clodsire': 9, 'Farigiraf': 9,
        'Koraidon': 9, 'Miraidon': 9, 'Oinkologne': 9,
        
        # Paradox Pokemon (Generation 9)
        'Great': 9, 'Brute': 9, 'Flutter': 9, 'Slither': 9, 'Sandy': 9, 'Scream': 9,
        'Iron': 9, 'Roaring': 9, 'Walking': 9, 'Gouging': 9, 'Raging': 9,
    }

def fix_pokemon_generations():
    """Fix generation assignments for Pokemon with generation -1"""
    
    # Load the Pokemon data
    with open('pokemon_data.json', 'r', encoding='utf-8') as f:
        pokemon_data = json.load(f)
    
    generation_mappings = load_generation_mappings()
    fixed_count = 0
    unknown_count = 0
    
    # Build a reverse lookup for Pokemon already in the data with correct generations
    base_generations = {}
    for name, data in pokemon_data.items():
        if data['generation'] != -1:
            base_name = get_base_pokemon_name(name)
            if base_name not in base_generations:
                base_generations[base_name] = data['generation']
    
    # Combine manual mappings with discovered mappings
    all_mappings = {**generation_mappings, **base_generations}
    
    print(f"Processing {len(pokemon_data)} Pokemon...")
    
    for name, data in pokemon_data.items():
        if data['generation'] == -1:
            base_name = get_base_pokemon_name(name)
            
            if base_name in all_mappings:
                new_generation = all_mappings[base_name]
                data['generation'] = new_generation
                fixed_count += 1
                print(f"Fixed {name} -> Generation {new_generation} (base: {base_name})")
            else:
                # Mark as unknown generation
                data['generation'] = "UG"
                unknown_count += 1
                print(f"Unknown: {name} -> UG (base: {base_name})")
    
    # Save the updated data
    with open('pokemon_data.json', 'w', encoding='utf-8') as f:
        json.dump(pokemon_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Fixed {fixed_count} Pokemon generations")
    print(f"❓ Marked {unknown_count} Pokemon as 'UG' (Unknown Generation)")
    print(f"💾 Updated pokemon_data.json")

if __name__ == "__main__":
    fix_pokemon_generations()
