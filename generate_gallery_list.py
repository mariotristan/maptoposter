#!/usr/bin/env python3
"""
Script to generate a JSON list of all poster files for the GitHub Pages gallery
"""

import json
import os
from pathlib import Path

def generate_posters_list():
    """Generate a JSON file listing all poster files"""
    posters_dir = Path("posters")
    posters_list = []
    
    # Popular Mexican cities for highlighting
    popular_cities = [
        'Mexico City', 'Guadalajara', 'Monterrey', 'Puebla', 'Tijuana',
        'León', 'Juárez', 'Torreón', 'Querétaro', 'San Luis Potosí'
    ]
    
    print("🔍 Scanning posters directory...")
    
    if not posters_dir.exists():
        print("❌ Posters directory not found!")
        return
    
    # Find all image files in the posters directory
    image_extensions = ['.png', '.jpg', '.jpeg', '.svg', '.pdf']
    poster_files = []
    
    for ext in image_extensions:
        poster_files.extend(posters_dir.glob(f"*{ext}"))
    
    print(f"📊 Found {len(poster_files)} poster files")
    
    for poster_file in sorted(poster_files):
        # Extract city name from filename - handle Mexican cities properly
        filename_parts = poster_file.stem.split('_')
        
        # Map known Mexican cities from filename format
        city_mapping = {
            'mexico': 'Mexico City',
            'guadalajara': 'Guadalajara',
            'monterrey': 'Monterrey', 
            'puebla': 'Puebla',
            'tijuana': 'Tijuana',
            'león': 'León',
            'juárez': 'Juárez',
            'torreón': 'Torreón',
            'querétaro': 'Querétaro',
            'nuevo': 'Nuevo Laredo'  # Handle nuevo_laredo case
        }
        
        if len(filename_parts) >= 1:
            city_key = filename_parts[0].lower()
            if city_key in city_mapping:
                city = city_mapping[city_key]
            elif city_key == 'nuevo' and len(filename_parts) >= 2 and filename_parts[1] == 'laredo':
                city = 'Nuevo Laredo'
            else:
                # Capitalize first letter for unknown cities
                city = filename_parts[0].replace('_', ' ').title()
        else:
            city = poster_file.stem.replace('_', ' ').title()
        
        # Extract theme (look for known theme patterns)
        theme = 'neon_cyberpunk'  # Default
        filename_lower = poster_file.stem.lower()
        if 'neon' in filename_lower and 'cyberpunk' in filename_lower:
            theme = 'neon_cyberpunk'
        elif 'contrast' in filename_lower:
            theme = 'contrast_zones'
        elif 'noir' in filename_lower:
            theme = 'noir'
        elif 'blueprint' in filename_lower:
            theme = 'blueprint'
        elif 'forest' in filename_lower:
            theme = 'forest'
        
        poster_info = {
            'city': city,
            'country': 'Mexico',
            'filename': poster_file.name,
            'path': f"posters/{poster_file.name}",
            'theme': theme,
            'isPopular': city in popular_cities,
            'size': poster_file.stat().st_size if poster_file.exists() else 0
        }
        
        posters_list.append(poster_info)
        print(f"✅ Added: {city}")
    
    # Write JSON file
    output_file = Path("posters-list.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(posters_list, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Generated {output_file} with {len(posters_list)} posters")
    print(f"📁 Popular cities found: {len([p for p in posters_list if p['isPopular']])}")
    
    return posters_list

def main():
    print("📋 Generating posters list for GitHub Pages...")
    print("=" * 50)
    
    posters_list = generate_posters_list()
    
    if posters_list:
        print("\n✨ Gallery is ready! Your GitHub Pages site will display:")
        print(f"   🎯 Total posters: {len(posters_list)}")
        print(f"   ⭐ Popular cities: {len([p for p in posters_list if p['isPopular']])}")
        print(f"   🎨 Themes: {len(set(p['theme'] for p in posters_list))}")
        print("\nTo enable GitHub Pages:")
        print("1. Push your code to GitHub")
        print("2. Go to Settings > Pages")
        print("3. Select 'Deploy from a branch' > 'main' > '/ (root)'")
        print("4. Your gallery will be live at: https://yourusername.github.io/maptoposter")
    else:
        print("\n⚠️  No posters found. Generate some posters first with:")
        print("   python generate_all_mexico_posters.py")

if __name__ == "__main__":
    main()