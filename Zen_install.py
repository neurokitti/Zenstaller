import os

# Define the path to the mozconfig file
mozconfig_path = os.path.join(os.getcwd(), "configs", "common", "mozconfig")

def modify_mozconfig(file_path):
    try:
        # Read the file content
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        # Step 1: Add a comment to the first line
        lines.insert(0, "# Added by script\n")
        
        # Step 2: Remove the seventh line (index 6 in zero-based indexing)
        if len(lines) > 7:  # Ensure the file has at least 7 lines
            lines.pop(7)

        # Write the updated content back to the file
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)
        
        print(f"Successfully modified {file_path}")

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    modify_mozconfig(mozconfig_path)
