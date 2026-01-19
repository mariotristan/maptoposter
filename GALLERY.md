# Mexico Map Poster Gallery 🇲🇽

A beautiful GitHub Pages gallery showcasing map posters of Mexican cities with cyberpunk neon styling.

## 🌐 Live Gallery

Visit the live gallery at: [https://originalankur.github.io/maptoposter](https://originalankur.github.io/maptoposter)

## 🎨 Features

- **Beautiful Grid Layout** - Responsive gallery showing all generated posters
- **Filter Options** - View all posters, popular cities, or recent additions
- **Interactive Cards** - Hover effects and download links for each poster
- **Mobile Responsive** - Looks great on all devices
- **Auto-Updated** - Gallery automatically updates when new posters are generated

## 🚀 How to Enable GitHub Pages

1. **Generate Posters**
   ```bash
   python generate_all_mexico_posters.py
   ```

2. **Update Gallery List**
   ```bash
   python generate_gallery_list.py
   ```

3. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add poster gallery"
   git push origin main
   ```

4. **Enable GitHub Pages**
   - Go to your repository Settings
   - Navigate to "Pages" section
   - Select "Deploy from a branch"
   - Choose "main" branch and "/ (root)" folder
   - Click "Save"

5. **Access Your Gallery**
   - Your gallery will be live at: `https://yourusername.github.io/repositoryname`
   - It may take a few minutes to become available

## 📁 Files

- `index.html` - Main gallery page with responsive design
- `generate_gallery_list.py` - Script to scan posters and generate JSON list
- `posters-list.json` - Auto-generated list of available posters (created when you run the generator)

## 🎯 Gallery Features

### Filter Options
- **All Posters** - Shows every generated poster
- **Popular Cities** - Highlights major Mexican cities
- **Recent** - Shows the 10 most recently processed posters

### Interactive Elements
- **Hover Effects** - Cards lift and images zoom on hover
- **Download Links** - Direct download buttons for each poster
- **Theme Badges** - Shows the styling theme used
- **Responsive Grid** - Adapts to different screen sizes

### Automatic Updates
The gallery automatically updates when you:
1. Generate new posters with `generate_all_mexico_posters.py`
2. Push changes to GitHub
3. GitHub Pages rebuilds the site

## 🔧 Customization

You can customize the gallery by editing `index.html`:

- **Colors** - Update the CSS gradient and color scheme
- **Layout** - Modify grid columns and card sizes  
- **Filters** - Add new filter categories
- **Content** - Change titles, descriptions, and footer text

## 📱 Mobile Support

The gallery is fully responsive and works beautifully on:
- 📱 Mobile phones
- 📱 Tablets  
- 💻 Laptops
- 🖥️ Desktop computers

## 🎨 Themes

Currently supports the **Neon Cyberpunk** theme, with future support planned for:
- Blueprint
- Forest
- Ocean
- Sunset
- And more!

---

**Made with ❤️ using the Map Poster Generator**