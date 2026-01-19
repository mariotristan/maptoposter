#!/usr/bin/env python3
"""
Script to clean up posters folder - remove non-Mexican cities and duplicates
"""

import os
import json
from pathlib import Path

def main():
    print("🧹 Cleaning up posters folder...")
    print("=" * 50)
    
    posters_dir = Path("posters")
    if not posters_dir.exists():
        print("❌ Posters directory not found!")
        return
    
    # Mexican cities (comprehensive list)
    mexican_cities = {
        'mexico_city', 'guadalajara', 'monterrey', 'puebla', 'tijuana',
        'león', 'juárez', 'torreón', 'querétaro', 'san_luis_potosí',
        'mérida', 'chihuahua', 'saltillo', 'aguascalientes', 'hermosillo',
        'mexicali', 'culiacán', 'acapulco', 'tlalnepantla', 'cancún',
        'centro', 'veracruz', 'oaxaca', 'tampico', 'cuernavaca',
        'xalapa', 'reynosa', 'tuxtla_gutiérrez', 'pachuca', 'toluca',
        'morelia', 'villahermosa', 'nuevo_laredo', 'mazatlán', 'irapuato',
        'cd_juárez', 'ciudad_juárez', 'juarez', 'nuevo_león', 'león_guanajuato'
    }
    
    # Non-Mexican cities to remove
    non_mexican_cities = {
        'barcelona', 'chicago', 'dubai', 'marrakech', 'melbourne',
        'mumbai', 'new_york', 'san_francisco', 'singapore', 'tokyo',
        'venice', 'washington'
    }
    
    # Get all poster files
    poster_files = list(posters_dir.glob("*.png")) + list(posters_dir.glob("*.jpg")) + list(posters_dir.glob("*.jpeg"))
    
    print(f"📊 Found {len(poster_files)} poster files")
    
    files_to_remove = []
    mexican_files = []
    
    # Track for duplicate detection
    city_theme_combinations = {}
    
    for poster_file in poster_files:
        # Extract city name from filename
        filename_lower = poster_file.stem.lower()
        
        # Check if it's a non-Mexican city
        is_non_mexican = any(city in filename_lower for city in non_mexican_cities)
        
        if is_non_mexican:
            files_to_remove.append(poster_file)
            print(f"🗑️  Removing non-Mexican city: {poster_file.name}")
            continue
        
        # Check if it's a Mexican city
        is_mexican = any(city in filename_lower for city in mexican_cities)
        
        if is_mexican:
            # Extract city and theme for duplicate detection
            parts = filename_lower.split('_')
            if len(parts) >= 3:
                city = parts[0]
                theme_parts = []
                for part in parts[1:]:
                    if not part.isdigit() and '20260' not in part:  # Skip timestamp parts
                        theme_parts.append(part)
                theme = '_'.join(theme_parts[:2])  # Take first 2 theme parts
                
                combination_key = f"{city}_{theme}"
                
                if combination_key in city_theme_combinations:
                    # Duplicate found - keep the newer one (by timestamp)
                    existing_file = city_theme_combinations[combination_key]
                    
                    # Compare timestamps in filenames
                    current_timestamp = ''.join([p for p in parts if '20260' in p])
                    existing_timestamp = ''.join([p for p in existing_file.stem.split('_') if '20260' in p])
                    
                    if current_timestamp > existing_timestamp:
                        # Current file is newer, remove the existing one
                        files_to_remove.append(existing_file)
                        city_theme_combinations[combination_key] = poster_file
                        mexican_files.append(poster_file)
                        print(f"🔄 Replacing older duplicate: {existing_file.name} -> {poster_file.name}")
                    else:
                        # Existing file is newer, remove current one
                        files_to_remove.append(poster_file)
                        print(f"🔄 Removing older duplicate: {poster_file.name}")
                        continue
                else:
                    city_theme_combinations[combination_key] = poster_file
                    mexican_files.append(poster_file)
            else:
                mexican_files.append(poster_file)
        else:
            # Unknown city, might be Mexican but not in our list
            print(f"❓ Unknown city (keeping): {poster_file.name}")
            mexican_files.append(poster_file)
    
    # Remove the files
    print(f"\n🗑️  Removing {len(files_to_remove)} files...")
    for file_to_remove in files_to_remove:
        try:
            file_to_remove.unlink()
            print(f"   ✅ Removed: {file_to_remove.name}")
        except Exception as e:
            print(f"   ❌ Error removing {file_to_remove.name}: {e}")
    
    print(f"\n✅ Cleanup complete!")
    print(f"   📊 Removed: {len(files_to_remove)} files")
    print(f"   📊 Remaining: {len(mexican_files)} Mexican city posters")
    
    # Regenerate posters-list.json
    print("\n🔄 Regenerating posters-list.json...")
    from generate_gallery_list import generate_posters_list
    generate_posters_list()
    
    print("\n🎉 All done! Your posters folder now contains only Mexican cities with no duplicates.")

if __name__ == "__main__":
    main()