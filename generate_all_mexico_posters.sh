#!/bin/bash

# Script to generate map posters for all Mexican cities
# Usage: ./generate_all_mexico_posters.sh

echo "🇲🇽 Starting batch generation of Mexico city map posters..."
echo "Theme: neon_cyberpunk"
echo "=========================================================="

# Check if mexico_cities.txt exists
if [ ! -f "mexico_cities.txt" ]; then
    echo "❌ Error: mexico_cities.txt file not found!"
    exit 1
fi

# Count total cities
total_cities=$(wc -l < mexico_cities.txt)
echo "📊 Total cities to process: $total_cities"
echo ""

# Initialize counters
current=0
success=0
failed=0

# Read each city from the file and generate poster
while IFS= read -r city || [ -n "$city" ]; do
    # Skip empty lines
    if [ -z "$city" ]; then
        continue
    fi
    
    current=$((current + 1))
    echo "🏙️  Processing city $current/$total_cities: $city"
    
    # Run the poster generation command
    if python create_map_poster.py --city "$city" --country "Mexico" --theme neon_cyberpunk; then
        success=$((success + 1))
        echo "✅ Successfully generated poster for $city"
    else
        failed=$((failed + 1))
        echo "❌ Failed to generate poster for $city"
    fi
    
    echo "----------------------------------------"
    
    # Optional: Add a small delay between requests to be respectful to APIs
    sleep 2
    
done < mexico_cities.txt

echo ""
echo "=========================================================="
echo "🏁 Batch generation complete!"
echo "📈 Summary:"
echo "   Total cities: $total_cities"
echo "   Successful: $success"
echo "   Failed: $failed"
echo "   Success rate: $(( success * 100 / total_cities ))%"
echo ""
echo "📁 Generated posters can be found in the 'posters/' directory"
echo "=========================================================="