#!/usr/bin/env python3
"""
Script to add variant classification to existing pokemon_data.json
"""
import json
import os

def classify_variant(pokemon_name: str) -> str:
    """Classify the variant type based on the Pokémon name"""
    name_lower = pokemon_name.lower()
    
    # Regional variants
    if "alola" in name_lower:
        return "Regional - Alolan"
    if "galar" in name_lower:
        return "Regional - Galarian"
    if "hisui" in name_lower:
        return "Regional - Hisuian"
    if "paldea" in name_lower:
        return "Regional - Paldean"
    
    # Gigantamax forms
    if "gmax" in name_lower or "gigantamax" in name_lower:
        return "Gigantamax"
    
    # Mega evolutions
    if "mega" in name_lower:
        return "Mega"
    
    # Special Pikachus
    if "pikachu" in name_lower and any(form in name_lower for form in ["-cosplay", "-rock-star", "-belle", "-pop-star", "-phd", "-libre", "-original-cap", "-hoenn-cap", "-sinnoh-cap", "-unova-cap", "-kalos-cap", "-alola-cap", "-partner-cap", "-world-cap"]):
        return "Special Pikachus"
    
    # Totem Pokemon
    if "totem" in name_lower:
        return "Totem Pokemon"
    
    # Paradox Pokemon (Iron/Ancient names or specific ones)
    if any(paradox in name_lower for paradox in ["iron-", "roaring-tail", "sandy-shocks", "scream-tail", "flutter-mane", "slither-wing", "great-tusk", "brute-bonnet", "walking-wake", "gouging-fire", "raging-bolt", "iron-treads", "iron-bundle", "iron-hands", "iron-jugulis", "iron-moth", "iron-thorns", "iron-valiant", "iron-leaves", "iron-boulder", "iron-crown"]):
        return "Paradox Pokemon"
    
    # Form variants
    if any(form in name_lower for form in ["-altered", "-origin", "-sky", "-land", "-attack", "-defense", "-speed", "-plant", "-sandy", "-trash", "-heat", "-wash", "-frost", "-fan", "-mow", "-incarnate", "-therian", "-ordinary", "-resolute", "-aria", "-pirouette", "-shield", "-blade", "-red-flower", "-yellow-flower", "-orange-flower", "-blue-flower", "-white-flower", "-primal", "-confined", "-unbound", "-baile", "-pom-pom", "-pau", "-sensu", "-disguised", "-busted", "-midday", "-midnight", "-dusk", "-ultra", "-dawn-wings", "-dusk-mane", "-complete", "-10", "-50", "-red", "-blue", "-yellow", "-white", "-orange", "-indigo", "-violet", "-crowned", "-eternamax", "-single-strike", "-rapid-strike", "-ice", "-shadow", "-rider", "-full-belly", "-hangry", "-gobbling", "-gulping", "-surfing", "-flying"]):
        return "Form Variants"
    
    # Size variants
    if any(size in name_lower for size in ["-small", "-large", "-super", "-average"]):
        return "Size Variants"
    
    return None

def main():
    """Add variant classification to pokemon_data.json"""
    data_file = "data_sources/pokemon_data.json"
    
    # Load existing data
    with open(data_file, 'r', encoding='utf-8') as f:
        pokemon_data = json.load(f)
    
    print(f"📊 Processing {len(pokemon_data)} Pokémon entries...")
    
    # Add variant field to each entry
    updated_count = 0
    variant_counts = {}
    
    for pokemon_name, data in pokemon_data.items():
        if isinstance(data, dict):
            # Classify variant
            variant = classify_variant(pokemon_name)
            
            # Add variant field
            data['variant'] = variant
            updated_count += 1
            
            # Count variants
            variant_key = variant if variant else 'Standard'
            variant_counts[variant_key] = variant_counts.get(variant_key, 0) + 1
    
    # Save updated data
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(pokemon_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Updated {updated_count} Pokémon entries with variant information")
    print(f"📈 Variant distribution:")
    for variant, count in sorted(variant_counts.items()):
        print(f"   {variant}: {count}")

if __name__ == "__main__":
    main()
