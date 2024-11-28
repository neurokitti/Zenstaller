import os
import subprocess
import shutil
import git

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

# Function to clone a repository
def clone_repo(repo_url, clone_to_path):
    try:
        print(f"Cloning {repo_url} into {clone_to_path}...")
        git.Repo.clone_from(repo_url, clone_to_path)
        print(f"Successfully cloned {repo_url}")
    except Exception as e:
        print(f"Error: Failed to clone {repo_url}. {e}")
        exit(1)

# Function to copy files and directories
def copy_files(src, dest):
    try:
        print(f"Copying files from {src} to {dest}...")
        shutil.copytree(src, dest, dirs_exist_ok=True)  # Copy files and directories
        print(f"Files and folders copied successfully from {src} to {dest}")
    except Exception as e:
        print(f"Error: Failed to copy files and folders from {src} to {dest}. {e}")
        exit(1)

# Function to run npm commands
def run_npm_commands():
    try:
        print("Running npm install...")
        subprocess.check_call(["npm", "i"])
        print("npm install completed.")

        print("Running npm run init...")
        subprocess.check_call(["npm", "run", "init"])
        print("npm run init completed.")

        print("Running npm run bootstrap...")
        subprocess.check_call(["npm", "run", "bootstrap"])
        print("npm run bootstrap completed.")
    except subprocess.CalledProcessError as e:
        print(f"Error: npm command failed. {e}")
        exit(1)

# Main installation process
if __name__ == "__main__":
    # Step 1: Clone the main repository
    clone_repo("https://github.com/neurokitti/desktop", desktop_folder)

    # Step 2: Navigate to the l10n folder and clone l10n-packs repository
    l10n_folder = os.path.join(desktop_folder, "l10n")
    clone_repo("https://github.com/neurokitti/l10n-packs", l10n_folder)

    # Step 3: Copy files and folders from l10n-packs into the l10n folder
    l10n_packs_folder = os.path.join(desktop_folder, "l10n-packs")
    copy_files(l10n_packs_folder, l10n_folder)

    # Step 4: Modify the mozconfig file
    modify_mozconfig(mozconfig_path, locales_path)

    # Step 5: Run npm commands (install, init, bootstrap)
    run_npm_commands()

    # Step 6: Final message
    print("Installation completed successfully.")
