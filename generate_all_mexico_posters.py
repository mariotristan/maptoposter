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
    
    # Check for cities file - prioritize full list
    cities_file = Path("mexico_cities_full.txt")
    if not cities_file.exists():
        cities_file = Path("mexico_cities.txt")
        if not cities_file.exists():
            print("❌ Error: No cities file found! Please create mexico_cities.txt or mexico_cities_full.txt")
            sys.exit(1)
    
    print(f"📋 Using cities file: {cities_file.name}")
    
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
    
    # Generate gallery list for GitHub Pages (always run to ensure it's up to date)
    print("🌐 Updating GitHub Pages gallery...")
    try:
        # Import and call the function directly for better error handling
        from generate_gallery_list import generate_posters_list
        posters_list = generate_posters_list()
        
        if posters_list and len(posters_list) > 0:
            print("✅ Gallery list updated successfully!")
            print(f"📊 Gallery now includes {len(posters_list)} posters")
            
            # Count themes
            themes = set(poster.get('theme', 'unknown') for poster in posters_list)
            theme_names = [poster.get('themeDisplay', poster.get('theme', 'Unknown')) for poster in posters_list]
            unique_theme_names = sorted(set(theme_names))
            print(f"🎨 Themes available: {', '.join(unique_theme_names)}")
            
            print("🌐 Your GitHub Pages gallery is ready to display all posters")
            
            if success > 0:
                print(f"🆕 {success} new posters added in this session")
        else:
            print("⚠️  Gallery list update failed - no posters found")
            
    except ImportError as e:
        print(f"⚠️  Could not import gallery generator: {e}")
        print("🔄 Falling back to subprocess call...")
        
        # Fallback to subprocess with virtual environment python
        try:
            venv_python = Path(__file__).parent / ".venv" / "bin" / "python"
            if venv_python.exists():
                result = subprocess.run([
                    str(venv_python), "generate_gallery_list.py"
                ], capture_output=True, text=True, cwd=Path(__file__).parent)
            else:
                result = subprocess.run([
                    "python", "generate_gallery_list.py"
                ], capture_output=True, text=True, cwd=Path(__file__).parent)
            
            if result.returncode == 0:
                print("✅ Gallery list updated successfully via subprocess!")
                print("🌐 Your GitHub Pages gallery is ready to display all posters")
                if success > 0:
                    print(f"🆕 {success} new posters added in this session")
            else:
                print("⚠️  Gallery list update failed:")
                print(f"     Error: {result.stderr.strip()}")
                
        except Exception as fallback_error:
            print(f"⚠️  Subprocess fallback also failed: {fallback_error}")
            
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