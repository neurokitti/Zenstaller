import os

# Define the path to the mozconfig file, assuming the script is run from the folder outside "desktop"
parent_folder = os.getcwd()  # Get the current working directory (assumed to be the parent folder of "desktop")
desktop_folder = os.path.join(parent_folder, "desktop")  # Path to the "desktop" folder
mozconfig_path = os.path.join(desktop_folder, "configs", "common", "mozconfig")

# Absolute path for the locales directory
locales_path = os.path.join(desktop_folder, "engine", "browser", "locales")

# Replace backslashes with forward slashes for compatibility in shell scripts
locales_path = locales_path.replace("\\", "/")

def modify_mozconfig(file_path, new_locales_path):
    try:
        # Read the file content
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Step 1: Ensure there are at least 7 lines, then replace line 7 (index 6)
        if len(lines) >= 7:
            lines[6] = f'ac_add_options --with-l10n-base="{new_locales_path}"\n'
        else:
            print("Error: The file doesn't have enough lines to modify line 7.")
            return

        # Step 2: Write the updated content back to the file
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)

        print(f"Successfully modified {file_path}")

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    modify_mozconfig(mozconfig_path, locales_path)
