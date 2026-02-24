import os
import re
import json
import shutil

# Configuration
SOURCE_DIR = "../manualBkup"
DEST_ASSETS_DIR = "assets"
OUTPUT_JSON = "data.json"

def simple_slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

projects = []
print("Starting extraction...")

if not os.path.exists(DEST_ASSETS_DIR):
    os.makedirs(DEST_ASSETS_DIR)

for filename in os.listdir(SOURCE_DIR):
    if filename.endswith(".html") and "Mikkopi - PORTFOLIO" in filename:
        filepath = os.path.join(SOURCE_DIR, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract Title
        title_match = re.search(r'<title>(.*?) — Mikkopi - PORTFOLIO</title>', content)
        if not title_match:
             title_match = re.search(r'<title>(.*?)Mikkopi - PORTFOLIO</title>', content)
        
        title = title_match.group(1) if title_match else "Untitled"
        if "Mikkopi - PORTFOLIO" in title or title.strip() == "":
             title = "Home" if "Mikkopi - PORTFOLIO.html" == filename else "Untitled"
             
        title = title.strip()
        slug = simple_slugify(title)
        print(f"Processing: {title} ({filename})")

        # Extract Description (First paragraph with significant length)
        description = ""
        # Look for <p> tags
        p_tags = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
        for p in p_tags:
            clean_p = re.sub(r'<[^>]+>', '', p).strip() # Remove inner tags
            if len(clean_p) > 50:
                description = clean_p
                break
        
        # Images
        companion_folder_name = filename.replace(".html", "_files")
        companion_folder_path = os.path.join(SOURCE_DIR, companion_folder_name)
        
        images = []
        if os.path.exists(companion_folder_path):
            all_files = []
            for img_f in os.listdir(companion_folder_path):
                if img_f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    full_path = os.path.join(companion_folder_path, img_f)
                    try:
                        size = os.path.getsize(full_path)
                        all_files.append((img_f, size, full_path))
                    except:
                        pass
            
            # Sort by size desc
            all_files.sort(key=lambda x: x[1], reverse=True)
            
            # Take top 10 largest items
            for img_name, size, full_path in all_files[:10]:
                 dest_folder = os.path.join(DEST_ASSETS_DIR, slug)
                 if not os.path.exists(dest_folder):
                     os.makedirs(dest_folder)
                 
                 try:
                    shutil.copy2(full_path, os.path.join(dest_folder, img_name))
                    images.append(f"{DEST_ASSETS_DIR}/{slug}/{img_name}")
                 except Exception as e:
                     print(f"Error copying {img_name}: {e}")

        projects.append({
            "title": title,
            "slug": slug,
            "description": description,
            "images": images,
            "original_file": filename
        })

with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(projects, f, indent=2)

print(f"Done. Extracted {len(projects)} projects.")
