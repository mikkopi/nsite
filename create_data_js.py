import json
import os

BASE_DIR = '/home/az/Antigravity projects/portof/new_portfolio'
DATA_FILE = os.path.join(BASE_DIR, 'data.json')
JS_FILE = os.path.join(BASE_DIR, 'js', 'data.js')

def create_js():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    # Create js directory if not exists
    os.makedirs(os.path.dirname(JS_FILE), exist_ok=True)
    
    js_content = f"const projects = {json.dumps(data, indent=4)};"
    
    with open(JS_FILE, 'w') as f:
        f.write(js_content)
    print(f"Created {JS_FILE}")

if __name__ == "__main__":
    create_js()
