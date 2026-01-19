#!/usr/bin/env python3
"""
Python script to generate map posters for all Mexican cities
Usage: python generate_all_mexico_posters.py
"""

import subprocess
import sys
import time
from pathlib import Path

def main():
    print("🇲🇽 Starting batch generation of Mexico city map posters...")
    print("Theme: neon_cyberpunk")
    print("=" * 56)
    
    # Check if mexico_cities.txt exists
    cities_file = Path("mexico_cities.txt")
    if not cities_file.exists():
        print("❌ Error: mexico_cities.txt file not found!")
        sys.exit(1)
    
    # Read all cities
    with open(cities_file, 'r', encoding='utf-8') as f:
        cities = [line.strip() for line in f if line.strip()]
    
    total_cities = len(cities)
    print(f"📊 Total cities to process: {total_cities}")
    print()
    
    # Initialize counters
    success = 0
    failed = 0
    
    # Process each city
    for i, city in enumerate(cities, 1):
        print(f"🏙️  Processing city {i}/{total_cities}: {city}")
        
        # Prepare command
        cmd = [
            "python", "create_map_poster.py",
            "--city", city,
            "--country", "Mexico",
            "--theme", "neon_cyberpunk"
        ]
        
        try:
            # Run the command
            result = subprocess.run(cmd, check=True, capture_output=False)
            success += 1
            print(f"✅ Successfully generated poster for {city}")
        except subprocess.CalledProcessError as e:
            failed += 1
            print(f"❌ Failed to generate poster for {city}")
            print(f"   Error: {e}")
        except KeyboardInterrupt:
            print("\n🛑 Process interrupted by user")
            break
        
        print("-" * 40)
        
        # Add delay between requests to be respectful to APIs
        time.sleep(2)
    
    # Print summary
    print()
    print("=" * 56)
    print("🏁 Batch generation complete!")
    print("📈 Summary:")
    print(f"   Total cities: {total_cities}")
    print(f"   Successful: {success}")
    print(f"   Failed: {failed}")
    if total_cities > 0:
        print(f"   Success rate: {success * 100 // total_cities}%")
    print()
    print("📁 Generated posters can be found in the 'posters/' directory")
    print("=" * 56)

if __name__ == "__main__":
    main()