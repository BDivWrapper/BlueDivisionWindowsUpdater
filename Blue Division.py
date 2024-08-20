import os
import sys
import requests
import zipfile
import shutil
import configparser
from tkinter import messagebox, Tk

# Hide main Tkinter window
root = Tk()
root.withdraw()

# Paths and URLs
SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
CONFIG_FILE = os.path.join(SCRIPT_DIR, 'config.txt')
GAME_DIR = os.path.join(SCRIPT_DIR, 'game')
GAME_EXECUTABLE = os.path.join(GAME_DIR, 'BDivision S.C.H.A.L.E. Defense.exe')

SCRIPT_REPO = "https://api.github.com/repos/BDivWrapper/BlueDivisionWindowsUpdater/releases/latest"
GAME_REPO = "https://api.github.com/repos/WhatIsThisG/BlueDivision_Release/releases/latest"

# Load or create config
config = configparser.ConfigParser()
if not os.path.exists(CONFIG_FILE):
    config['VERSIONS'] = {'script_version': '1.0.0', 'game_version': 'None'}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
else:
    config.read(CONFIG_FILE)

def prompt_user(message):
    return messagebox.askyesno("Update Available", message)

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

def flatten_directory(dir):
    while True:
        subdirs = [d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]
        if len(subdirs) == 1 and not any(os.path.isfile(os.path.join(dir, f)) for f in os.listdir(dir)):
            subdir_path = os.path.join(dir, subdirs[0])
            for item in os.listdir(subdir_path):
                shutil.move(os.path.join(subdir_path, item), dir)
            os.rmdir(subdir_path)
        else:
            break

def update_script(latest_version, download_url):
    if prompt_user(f"A new script version ({latest_version}) is available. Would you like to update?"):
        temp_filename = os.path.join(SCRIPT_DIR, 'tmp_bdiv.exe')
        download_file(download_url, temp_filename)

        # Update config with new script version before replacing the current script
        config['VERSIONS']['script_version'] = latest_version
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)

        # Replace current script with the new version
        new_script_path = os.path.join(SCRIPT_DIR, 'tmp_bdiv.exe')
        current_script_path = os.path.abspath(sys.argv[0])
        os.replace(new_script_path, current_script_path)

        messagebox.showinfo("Update", "The script has been updated. Please restart the application.")
        os.startfile(current_script_path)
        exit(0)

def update_game(latest_version, download_url):
    if prompt_user(f"A new game version ({latest_version}) is available. Would you like to update?"):
        zip_filename = os.path.join(SCRIPT_DIR, 'BlueDivision.zip')
        download_file(download_url, zip_filename)

        # Clear the game directory
        if os.path.exists(GAME_DIR):
            shutil.rmtree(GAME_DIR)
        os.makedirs(GAME_DIR)

        # Extract the new game version
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(GAME_DIR)
        os.remove(zip_filename)

        # Flatten the directory structure
        flatten_directory(GAME_DIR)

        # Update config with new game version
        config['VERSIONS']['game_version'] = latest_version
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)

        messagebox.showinfo("Update", "The game has been updated.")

def check_for_updates():
    try:
        # Check for script updates
        script_response = requests.get(SCRIPT_REPO)
        script_data = script_response.json()
        latest_script_version = script_data['tag_name']
        script_download_url = next(asset['browser_download_url'] for asset in script_data['assets'] if asset['name'].endswith('.exe'))

        current_script_version = config['VERSIONS']['script_version']
        if latest_script_version != current_script_version:
            update_script(latest_script_version, script_download_url)
    except Exception:
        messagebox.showwarning("Offline Mode", "Could not check for script updates")

    try:
        # Check for game updates
        game_response = requests.get(GAME_REPO)
        game_data = game_response.json()
        latest_game_version = game_data['tag_name']
        game_download_url = next(asset['browser_download_url'] for asset in game_data['assets'] if asset['name'].endswith('.zip'))

        current_game_version = config['VERSIONS']['game_version']
        if latest_game_version != current_game_version:
            update_game(latest_game_version, game_download_url)

        # Save any changes to the config file
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)

    except Exception:
        messagebox.showwarning("Offline Mode", "Could not check for game updates.")

def launch_game():
    if os.path.exists(GAME_EXECUTABLE):
        os.startfile(GAME_EXECUTABLE)
    else:
        messagebox.showerror("Error", "Game executable not found. Please update the game or check the installation.")

if __name__ == "__main__":
    check_for_updates()
    launch_game()
