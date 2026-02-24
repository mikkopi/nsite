import json
import os

# Paths
BASE_DIR = '/home/az/Antigravity projects/portof/new_portfolio'
DATA_FILE = os.path.join(BASE_DIR, 'data.json')
INDEX_FILE = os.path.join(BASE_DIR, 'index.html')
PROJECT_FILE = os.path.join(BASE_DIR, 'project.html')

def sync_data():
    # 1. Read data.json
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    print(f"Loaded {len(data)} projects from data.json")
    
    # 2. Prepare replacement string
    # We want it to look like: const projects = [ ... ];
    projects_json = json.dumps(data, indent=4)
    replacement_string = f"const projects = {projects_json};"

    # 3. Update index.html
    update_file(INDEX_FILE, replacement_string)

    # 4. Update project.html
    update_file(PROJECT_FILE, replacement_string)

def update_file(filepath, replacement_string):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find start
    start_marker = "const projects = ["
    start_idx = content.find(start_marker)
    
    if start_idx == -1:
        print(f"Could not find '{start_marker}' in {filepath}")
        return
    
    # Find end
    # We look for the next "];" after the start
    end_marker = "];"
    end_idx = content.find(end_marker, start_idx)
    
    if end_idx == -1:
        print(f"Could not find closing '{end_marker}' in {filepath}")
        return
    
    # Include the closing marker in the replacement zone?
    # Original: const projects = [ ... ];
    # Replacement: const projects = [ ... ];
    # So we replace from start_idx to end_idx + len(end_marker)
    
    old_section = content[start_idx : end_idx + len(end_marker)]
    new_content = content.replace(old_section, replacement_string)
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

if __name__ == "__main__":
    sync_data()
