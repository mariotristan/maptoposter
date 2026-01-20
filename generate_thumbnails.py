#!/usr/bin/env python3
"""
Script to generate thumbnails for all posters in the gallery
"""

import os
import json
from pathlib import Path
from PIL import Image

def generate_thumbnails():
    """Generate thumbnails for all poster images"""
    posters_dir = Path("posters")
    thumbs_dir = Path("thumbnails")
    
    print("🖼️  Generating thumbnails for better performance...")
    print("=" * 60)
    
    # Create thumbnails directory if it doesn't exist
    thumbs_dir.mkdir(exist_ok=True)
    
    # Thumbnail settings
    THUMB_SIZE = (400, 300)  # Width x Height for gallery cards
    QUALITY = 85  # JPEG quality (1-100)
    
    if not posters_dir.exists():
        print("❌ Posters directory not found!")
        return []
    
    # Find all image files
    image_extensions = ['.png', '.jpg', '.jpeg']
    poster_files = []
    
    for ext in image_extensions:
        poster_files.extend(posters_dir.glob(f"*{ext}"))
    
    print(f"📊 Found {len(poster_files)} poster files")
    
    generated_count = 0
    skipped_count = 0
    
    for poster_file in poster_files:
        # Create thumbnail filename
        thumb_filename = f"{poster_file.stem}_thumb.jpg"
        thumb_path = thumbs_dir / thumb_filename
        
        # Check if thumbnail already exists and is newer than original
        if thumb_path.exists():
            poster_time = poster_file.stat().st_mtime
            thumb_time = thumb_path.stat().st_mtime
            
            if thumb_time >= poster_time:
                print(f"⏭️  Skipping (exists): {poster_file.name}")
                skipped_count += 1
                continue
        
        try:
            # Open and process image
            with Image.open(poster_file) as img:
                # Convert RGBA to RGB if necessary (for PNG with transparency)
                if img.mode in ('RGBA', 'LA'):
                    # Create white background
                    white_bg = Image.new('RGB', img.size, 'white')
                    if img.mode == 'RGBA':
                        white_bg.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
                    else:
                        white_bg.paste(img)
                    img = white_bg
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Calculate thumbnail size maintaining aspect ratio
                img_ratio = img.width / img.height
                thumb_ratio = THUMB_SIZE[0] / THUMB_SIZE[1]
                
                if img_ratio > thumb_ratio:
                    # Image is wider, fit to width
                    new_width = THUMB_SIZE[0]
                    new_height = int(THUMB_SIZE[0] / img_ratio)
                else:
                    # Image is taller, fit to height
                    new_height = THUMB_SIZE[1]
                    new_width = int(THUMB_SIZE[1] * img_ratio)
                
                # Resize with high-quality resampling
                thumbnail = img.resize((new_width, new_height), Image.LANCZOS)
                
                # Create final thumbnail with padding if needed
                final_thumb = Image.new('RGB', THUMB_SIZE, 'white')
                
                # Center the resized image
                x_offset = (THUMB_SIZE[0] - new_width) // 2
                y_offset = (THUMB_SIZE[1] - new_height) // 2
                final_thumb.paste(thumbnail, (x_offset, y_offset))
                
                # Save thumbnail
                final_thumb.save(thumb_path, 'JPEG', quality=QUALITY, optimize=True)
                
                # Get file sizes
                original_size = poster_file.stat().st_size
                thumb_size = thumb_path.stat().st_size
                reduction = (1 - thumb_size / original_size) * 100
                
                print(f"✅ Generated: {thumb_filename}")
                print(f"   📏 Size: {new_width}x{new_height} (from {img.width}x{img.height})")
                print(f"   💾 Size: {thumb_size//1024}KB (was {original_size//1024}KB, {reduction:.1f}% reduction)")
                
                generated_count += 1
                
        except Exception as e:
            print(f"❌ Error processing {poster_file.name}: {e}")
    
    print()
    print("=" * 60)
    print(f"🎉 Thumbnail generation complete!")
    print(f"   ✅ Generated: {generated_count}")
    print(f"   ⏭️  Skipped: {skipped_count}")
    print(f"   📁 Thumbnails saved to: {thumbs_dir}")
    
    # Calculate total savings
    if generated_count > 0:
        total_original = sum(f.stat().st_size for f in poster_files)
        total_thumbs = sum(f.stat().st_size for f in thumbs_dir.glob("*.jpg"))
        total_savings = (1 - total_thumbs / total_original) * 100 if total_original > 0 else 0
        
        print(f"   💾 Total size reduction: {total_savings:.1f}%")
        print(f"   🚀 Gallery will load {total_savings:.1f}% faster!")

def update_posters_json_with_thumbnails():
    """Update the posters JSON to include thumbnail paths"""
    print("\n🔄 Updating posters-list.json with thumbnail paths...")
    
    json_file = Path("posters-list.json")
    thumbs_dir = Path("thumbnails")
    
    if not json_file.exists():
        print("❌ posters-list.json not found!")
        return
    
    # Read current JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        posters = json.load(f)
    
    updated_count = 0
    
    for poster in posters:
        # Generate expected thumbnail filename
        poster_filename = Path(poster['filename'])
        thumb_filename = f"{poster_filename.stem}_thumb.jpg"
        thumb_path = thumbs_dir / thumb_filename
        
        if thumb_path.exists():
            poster['thumbnailPath'] = f"thumbnails/{thumb_filename}"
            updated_count += 1
        else:
            # Fallback to original image if thumbnail doesn't exist
            poster['thumbnailPath'] = poster['path']
    
    # Write updated JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(posters, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Updated {updated_count} entries with thumbnail paths")

def main():
    print("🖼️  THUMBNAIL GENERATOR")
    print("🚀 Optimizing gallery performance with thumbnails")
    print("=" * 60)
    
    # Check if PIL is available
    try:
        from PIL import Image
        print("✅ PIL (Pillow) found - ready to generate thumbnails")
    except ImportError:
        print("❌ PIL (Pillow) not found!")
        print("📦 Install with: pip install Pillow")
        return
    
    # Generate thumbnails
    generate_thumbnails()
    
    # Update JSON
    update_posters_json_with_thumbnails()
    
    print("\n🎉 All done! Your gallery is now optimized for fast loading!")
    print("💡 Don't forget to add the 'thumbnails/' folder to your git repo")

if __name__ == "__main__":
    main()