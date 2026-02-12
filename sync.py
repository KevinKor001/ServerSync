import os
import lib.questionary as qs
import json
from os import stat
from pathlib import Path
from lib.ftp import SFTPSync 


def load_config(filename=".SyncNode.config"):
    path = Path(filename)
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return None

def get_smart_staged_paths(root_dir, config):
    blacklist = config.get("blacklist", [])
    auto_sync = config.get("autoSync", [])
    
    choices = []
    
    # Use .iterdir() to stay in the ROOT only
    for p in Path(root_dir).iterdir():
        rel_path = p.name
        
        if rel_path in blacklist or rel_path.startswith('.'):
            continue
            
        is_auto = rel_path in auto_sync
        choices.append(qs.Choice(rel_path, checked=is_auto))

    return qs.checkbox("Select top-level folders/files to sync:", choices=choices).ask()
config = load_config()
def handle_upload():
    current_dir = Path.cwd()
    config = load_config()

    if config is None:
        print("\n[!] Configuration Missing")
        print(f"[*] No '.SyncNode.config' found in: {current_dir}")
        print("[*] Please run 'ServerSync init' (or setup) in this directory first.\n")
        return    
    print(f"[*] Scanning for files in: {current_dir}")
    
    selected = get_smart_staged_paths(current_dir, config)
    
    if not selected:
        print("[~] No files selected for sync.")
        return
    client = SFTPSync(config['ip'], config['user'], config['password'], config['port'])
    if client.connect() is True:
        for item in selected:
            local_path = current_dir / item
            
            if local_path.is_dir():
                client.upload_directory(str(local_path), config['directory'])
            else:
                client.upload_with_progress(str(local_path), config['directory'])
        client.disconnect()
        print("\n[✔] Staged Sync Complete!")
