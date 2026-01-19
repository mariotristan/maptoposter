#!/usr/bin/env python3
"""
Python script to generate map posters for all Mexican cities
Usage: python generate_all_mexico_posters.py
"""

import subprocess
import sys
import time
from pathlib import Path
from tqdm import tqdm
import json

def main():
    print("🇲🇽" + "=" * 56 + "🇲🇽")
    print("🎨          MEXICO MAP POSTER GENERATOR          🎨")
    print("🇲🇽" + "=" * 56 + "🇲🇽")
    print()
    print("🎨 Theme: neon_cyberpunk")
    print("🌮 Country: Mexico")
    print("✨ Enhanced with beautiful progress tracking!")
    print()
    print("─" * 60)
    
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
    
    # Process each city with enhanced progress bar
    print("🚀 Starting poster generation with enhanced progress tracking...")
    print()
    
    # Clean progress bar format for better visibility
    bar_format = "{l_bar}{bar:30}{r_bar}"
    
    with tqdm(cities, 
              desc="🎨 Generating Posters", 
              unit=" cities", 
              ncols=100,
              bar_format=bar_format,
              colour='green',
              ascii=False,
              leave=True,
              dynamic_ncols=True) as pbar:
        
        for city in pbar:
            # Update description with current city (clean formatting)
            city_display = f"{city[:20]}{'...' if len(city) > 20 else ''}"
            pbar.set_description(f"🎨 Processing: {city_display}")
            
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
                # Clean postfix with essential info
                pbar.set_postfix_str(f"✅{success} ❌{failed}")
                
            except subprocess.CalledProcessError as e:
                failed += 1
                pbar.set_postfix_str(f"✅{success} ❌{failed}")
                
                # Show error cleanly
                tqdm.write(f"\n🔴 Failed: {city} - {str(e)[:60]}{'...' if len(str(e)) > 60 else ''}")
                
            except KeyboardInterrupt:
                tqdm.write("\n🛑 Process interrupted by user")
                break
            
            # Add delay between requests to be respectful to APIs
            time.sleep(2)
    
    # Print enhanced summary
    print()
    print("🎉" + "=" * 58 + "🎉")
    print("🏁                BATCH GENERATION COMPLETE!                🏁")
    print("🎉" + "=" * 58 + "🎉")
    print()
    
    # Calculate success rate
    success_rate = (success * 100 // total_cities) if total_cities > 0 else 0
    
    # Choose emoji based on success rate
    if success_rate >= 90:
        rate_emoji = "🌟"
        status_emoji = "🚀"
    elif success_rate >= 70:
        rate_emoji = "👍"
        status_emoji = "✨"
    elif success_rate >= 50:
        rate_emoji = "⚠️"
        status_emoji = "🔧"
    else:
        rate_emoji = "🔴"
        status_emoji = "🛠️"
    
    print(f"📊 GENERATION STATISTICS {status_emoji}")
    print("─" * 40)
    print(f"   🎯 Total cities processed: {total_cities}")
    print(f"   ✅ Successfully generated: {success}")
    print(f"   ❌ Failed generations: {failed}")
    print(f"   {rate_emoji} Success rate: {success_rate}%")
    print()
    print(f"📁 Generated posters location:")
    print(f"   └─ 📂 ./posters/ directory")
    print()
    
    # Add motivational message based on results
    if success_rate >= 90:
        print("🌟 Excellent work! Almost all posters generated successfully!")
    elif success_rate >= 70:
        print("👏 Great job! Most posters were generated successfully!")
    elif success_rate >= 50:
        print("💪 Good effort! You may want to check the failed cities.")
    else:
        print("🔧 Some issues occurred. Check the errors above for troubleshooting.")
    
    print()
    print("🇲🇽" + "=" * 56 + "🇲🇽")
    
    # Generate gallery list for GitHub Pages
    if success > 0:
        print("🌐 Updating GitHub Pages gallery...")
        try:
            result = subprocess.run([
                "python", "generate_gallery_list.py"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Gallery list updated successfully!")
                print("🌐 Your GitHub Pages gallery is ready to display new posters")
            else:
                print("⚠️  Gallery list update failed, but posters were generated successfully")
        except Exception as e:
            print(f"⚠️  Could not update gallery list: {e}")
        
        print()
        print("🚀 Next steps:")
        print("   1. Push your changes to GitHub")
        print("   2. Enable GitHub Pages in repository settings")
        print("   3. Your gallery will be live at: https://yourusername.github.io/maptoposter")
    
    print()
    print("🇲🇽" + "=" * 56 + "🇲🇽")

if __name__ == "__main__":
    main()