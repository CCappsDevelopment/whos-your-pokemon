#!/usr/bin/env python3
"""
Script to clean up pokemon_data.json by removing alternate forms
but keeping regional variants (Alola, Galar, Hisui, Paldea)
"""

import json
import re

def should_remove_pokemon(name):
    """
    Determine if a Pokemon should be removed based on its name.
    Returns True if it should be removed, False if it should be kept.
    """
    
    # Keep regional variants
    regional_patterns = [
        r'-alola',
        r'-galar', 
        r'-hisui',
        r'-paldea'
    ]
    
    for pattern in regional_patterns:
        if re.search(pattern, name.lower()):
            return False
    
    # Remove alternate forms
    remove_patterns = [
        r'-mega',           # Mega evolutions
        r'mega-',           # Mega evolutions (different format)
        r'-gigantamax',     # Gigantamax forms
        r'gigantamax-',     # Gigantamax forms (different format)
        r'-gmax',           # Short form of Gigantamax
        r'gmax-',           # Short form of Gigantamax
        r'-primal',         # Primal forms
        r'primal-',         # Primal forms
        r'-origin',         # Origin formes
        r'origin-',         # Origin formes
        r'-therian',        # Therian formes
        r'therian-',        # Therian formes
        r'-zen',            # Zen mode
        r'zen-',            # Zen mode
        r'-eternamax',      # Eternamax
        r'eternamax-',      # Eternamax
        r'-ultra',          # Ultra forms
        r'ultra-',          # Ultra forms
        r'-power-construct', # Zygarde power construct
        r'power-construct-', # Zygarde power construct
        r'-complete',       # Zygarde complete
        r'complete-',       # Zygarde complete
        r'-10-',            # Zygarde 10%
        r'-50-',            # Zygarde 50%
        r'-dusk',           # Necrozma dusk mane
        r'dusk-',           # Necrozma dusk mane
        r'-dawn',           # Necrozma dawn wings
        r'dawn-',           # Necrozma dawn wings
        r'-attack',         # Deoxys attack forme
        r'attack-',         # Deoxys attack forme
        r'-defense',        # Deoxys defense forme
        r'defense-',        # Deoxys defense forme
        r'-speed',          # Deoxys speed forme
        r'speed-',          # Deoxys speed forme
        r'-sky',            # Shaymin sky forme
        r'sky-',            # Shaymin sky forme
        r'-heat',           # Rotom heat
        r'heat-',           # Rotom heat
        r'-wash',           # Rotom wash
        r'wash-',           # Rotom wash
        r'-frost',          # Rotom frost
        r'frost-',          # Rotom frost
        r'-fan',            # Rotom fan
        r'fan-',            # Rotom fan
        r'-mow',            # Rotom mow
        r'mow-',            # Rotom mow
        r'-original',       # Original forms (like Magearna)
        r'original-',       # Original forms
        r'-cap',            # Pikachu cap variants
        r'cap-',            # Pikachu cap variants
        r'-totem',          # Totem Pokemon
        r'totem-',          # Totem Pokemon
        r'-altered',        # Giratina altered forme
        r'altered-',        # Giratina altered forme
        r'-solo',           # Wishiwashi solo form
        r'solo-',           # Wishiwashi solo form
        r'-school',         # Wishiwashi school form
        r'school-',         # Wishiwashi school form
        r'-disguised',      # Mimikyu disguised form
        r'disguised-',      # Mimikyu disguised form
        r'-busted',         # Mimikyu busted form
        r'busted-',         # Mimikyu busted form
        r'-standard',       # Standard forms when there are variants
        r'standard-',       # Standard forms when there are variants
        r'-female',         # Gender variants
        r'female-',         # Gender variants
        r'-male',           # Gender variants
        r'male-',           # Gender variants
        r'-striped',        # Striped variants
        r'striped-',        # Striped variants
        r'-segment',        # Segment variants
        r'segment-',        # Segment variants
        r'-white',          # Color variants (like White-Striped)
        r'white-',          # Color variants
        r'-plumage',        # Plumage variants
        r'plumage-',        # Plumage variants
        r'-roaming',        # Roaming forms
        r'roaming-',        # Roaming forms
        r'-bloodmoon',      # Bloodmoon forms
        r'bloodmoon-',      # Bloodmoon forms
        r'-mask',           # Mask variants
        r'mask-',           # Mask variants
        r'-terastal',       # Terastal forms
        r'terastal-',       # Terastal forms
        r'-stellar',        # Stellar forms
        r'stellar-',        # Stellar forms
        r'-wellspring',     # Wellspring variants
        r'wellspring-',     # Wellspring variants
        r'-hearthflame',    # Hearthflame variants
        r'hearthflame-',    # Hearthflame variants
        r'-cornerstone',    # Cornerstone variants
        r'cornerstone-',    # Cornerstone variants
        r'-hero',           # Hero forms
        r'hero-',           # Hero forms
        r'-family',         # Family variants
        r'family-',         # Family variants
        r'-breed',          # Breed variants
        r'breed-',          # Breed variants
        r'-droopy',         # Droopy forms
        r'droopy-',         # Droopy forms
        r'-stretchy',       # Stretchy forms
        r'stretchy-',       # Stretchy forms
        r'-combat',         # Combat forms
        r'combat-',         # Combat forms
        r'-blaze',          # Blaze forms
        r'blaze-',          # Blaze forms
        r'-aqua',           # Aqua forms
        r'aqua-',           # Aqua forms
    ]
    
    # Special cases that should be removed but don't follow the pattern above
    special_remove_cases = [
        'Giratina-Altered',          # Keep only the normal Giratina
        'Zygarde-50',                # Keep only the normal Zygarde
        'Wishiwashi-Solo',           # Keep only the normal Wishiwashi
        'Dialga-Origin',             # Remove origin forms
        'Palkia-Origin',             # Remove origin forms  
        'Enamorus-Therian',          # Remove therian forms
        'Basculin-White-Striped',    # Remove alternate Basculin
        'Basculegion-Female',        # Remove gender variants
        'Oinkologne-Female',         # Remove gender variants
        'Dudunsparce-Three-Segment', # Remove segment variants
        'Squawkabilly-Green-Plumage', # Remove plumage variants
        'Squawkabilly-Blue-Plumage',  # Remove plumage variants
        'Squawkabilly-Yellow-Plumage', # Remove plumage variants
        'Squawkabilly-White-Plumage', # Remove plumage variants
        'Gimmighoul-Roaming',        # Remove roaming form
        'Ursaluna-Bloodmoon',        # Remove bloodmoon form
        # Remove all Pikachu cap variants (they have -Cap in name)
        'Pikachu-Original-Cap',
        'Pikachu-Hoenn-Cap',
        'Pikachu-Sinnoh-Cap',
        'Pikachu-Unova-Cap',
        'Pikachu-Kalos-Cap',
        'Pikachu-Alola-Cap',  # This one is regional but also a cap variant
    ]
    
    if name in special_remove_cases:
        return True
    
    for pattern in remove_patterns:
        if re.search(pattern, name.lower()):
            return True
    
    return False

def clean_pokemon_data():
    """Clean the pokemon_data.json file"""
    
    # Load the current data
    with open('pokemon_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Original count: {len(data)} Pokemon")
    
    # Filter out alternate forms
    cleaned_data = {}
    removed_pokemon = []
    
    for name, url in data.items():
        if should_remove_pokemon(name):
            removed_pokemon.append(name)
        else:
            cleaned_data[name] = url
    
    print(f"Cleaned count: {len(cleaned_data)} Pokemon")
    print(f"Removed: {len(removed_pokemon)} Pokemon")
    
    # Show some examples of what was removed
    if removed_pokemon:
        print("\nExamples of removed Pokemon:")
        for pokemon in sorted(removed_pokemon)[:20]:  # Show first 20
            print(f"  - {pokemon}")
        if len(removed_pokemon) > 20:
            print(f"  ... and {len(removed_pokemon) - 20} more")
    
    # Save the cleaned data
    with open('pokemon_data_cleaned.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nCleaned data saved to pokemon_data_cleaned.json")
    
    # Show some examples of regional variants that were kept
    regional_variants = [name for name in cleaned_data.keys() 
                        if any(region in name.lower() for region in ['alola', 'galar', 'hisui', 'paldea'])]
    
    if regional_variants:
        print(f"\nKept {len(regional_variants)} regional variants:")
        for variant in sorted(regional_variants)[:10]:  # Show first 10
            print(f"  - {variant}")
        if len(regional_variants) > 10:
            print(f"  ... and {len(regional_variants) - 10} more")

if __name__ == "__main__":
    clean_pokemon_data()
