import os
import subprocess
import shutil

# Define the parent folder (the script will be run from the folder outside "desktop")
parent_folder = os.getcwd()  # Get the current working directory (assumed to be the parent folder of "desktop")
desktop_folder = os.path.join(parent_folder, "desktop")  # Path to the "desktop" folder
mozconfig_path = os.path.join(desktop_folder, "configs", "common", "mozconfig")

# Absolute path for the locales directory
locales_path = os.path.join(desktop_folder, "engine", "browser", "locales")

# Replace backslashes with forward slashes for compatibility in shell scripts
locales_path = locales_path.replace("\\", "/")

# Function to modify the mozconfig file
def modify_mozconfig(file_path, new_locales_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        if len(lines) >= 7:
            lines[6] = f'ac_add_options --with-l10n-base="{new_locales_path}"\n'
        else:
            print("Error: The file doesn't have enough lines to modify line 7.")
            return

        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)

        print(f"Successfully modified {file_path}")

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to clone a repository using git command
def clone_repo(repo_url, clone_to_path):
    try:
        print(f"Cloning {repo_url} into {clone_to_path}...")
        subprocess.check_call(["git", "clone", repo_url, clone_to_path])  # Use git command to clone
        print(f"Successfully cloned {repo_url}")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to clone {repo_url}. {e}")
        exit(1)

# Function to copy files and directories
def copy_files(src, dest):
    try:
        print(f"Copying files from {src} to {dest}...")
        # Check if source folder exists before copying
        if not os.path.exists(src):
            print(f"Error: Source folder does not exist: {src}")
            exit(1)

        

        # If the destination already has the l10n-packs folder, remove it
        if os.path.exists(dest):
            print(f"Destination folder exists, removing: {dest}")
            shutil.rmtree(dest)

        # Copy all files and subdirectories, but not the root folder itself
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dest, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)  # Copy subdirectories
            else:
                shutil.copy2(s, d)  # Copy files

        print(f"Files and folders copied successfully from {src} to {dest}")
    except Exception as e:
        print(f"Error: Failed to copy files and folders from {src} to {dest}. {e}")
        exit(1)


# Function to run npm commands
# Function to run npm commands
def run_npm_commands():
    try:
        os.chdir(desktop_folder)
        print("Current Directory:", os.getcwd())

        print("Running npm install...")
        subprocess.run(["npm", "install"], shell=True, check=True)
        print("npm install completed.")

        os.chdir(desktop_folder)
        print("Current Directory:", os.getcwd())
        print("Running npm run init...")
        subprocess.run(["npm", "run", "init"], shell=True, check=True)
        print("npm run init completed.")

        os.chdir(desktop_folder)
        print("Current Directory:", os.getcwd())
        print("Running npm run bootstrap...")
        subprocess.run(["npm", "run", "bootstrap"], shell=True, check=True)
        print("npm run bootstrap completed.")

        os.chdir(desktop_folder)
        print("Current Directory:", os.getcwd())
        print("Running npm run bootstrap...")
        subprocess.run(["npm", "run", "build"], shell=True, check=True)
        print("npm run bootstrap completed.")

    except subprocess.CalledProcessError as e:
        print(f"Error: npm command failed. {e}")
        exit(1)

# Function to copy l10n-packs contents to l10n folder
def copy_l10n_packs(src, dest):
    try:
        print(f"Copying l10n-packs contents from {src} to {dest}...")
        
        # Check if source folder exists
        if not os.path.exists(src):
            print(f"Error: Source folder does not exist: {src}")
            exit(1)
        
        # Ensure destination folder exists
        os.makedirs(dest, exist_ok=True)

        # Copy all files and subdirectories from src to dest
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dest, item)
            
            if os.path.isdir(s):
                # If it's a directory, copy entire directory
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                # If it's a file, copy the file
                shutil.copy2(s, d)

        print(f"Successfully copied l10n-packs contents to {dest}")
    
    except Exception as e:
        print(f"Error: Failed to copy l10n-packs contents. {e}")
        exit(1)
        
# Main installation process
if __name__ == "__main__":
    # Step 1: Clone the main repository
    default_desktop_repo = "https://github.com/neurokitti/desktop"
    foreked_repo = input(f"Paste a link to your fork of the desktop repo (press Enter to use default: {default_desktop_repo}): ").strip()
    desktop_repo = foreked_repo if foreked_repo else default_desktop_repo
    clone_repo(desktop_repo, desktop_folder)


    # Step 2: Navigate to the l10n folder and clone l10n-packs repository
    default_l10n_repo = "https://github.com/neurokitti/l10n-packs"
    foreked_repo = input(f"Paste a link to your fork of the l10n-packs repo (press Enter to use default: {default_desktop_repo}): ").strip()
    l10n_repo = foreked_repo if foreked_repo else default_l10n_repo
    l10n_folder = os.path.join(desktop_folder, "l10n")
    l10n_packs_folder = os.path.join(parent_folder, "l10n-packs")  # Temporary location
    clone_repo(l10n_repo, l10n_packs_folder)

    # Step 3: Copy contents from l10n-packs to l10n folder
    copy_l10n_packs(l10n_packs_folder, l10n_folder)
 
    # Step 4: Modify the mozconfig file
    modify_mozconfig(mozconfig_path, locales_path)

    # Step 5: Run npm commands (install, init, bootstrap)
    run_npm_commands()

    # Step 6: Final message
    print("Installation completed successfully.")
