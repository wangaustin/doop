import os
import platform
import datetime
import subprocess

def is_hidden(filepath):
    """Checks if a file is hidden based on OS-specific criteria."""
    if os.path.basename(filepath).startswith("."):
        return True  # Dot files are hidden on Unix-like systems
    if platform.system() == "Windows":
        try:
            attrs = os.stat(filepath).st_file_attributes
            return bool(attrs & 2)  # Check for the hidden attribute
        except AttributeError:
            pass  # Handle cases where the attribute isn't available
    elif platform.system() in ["Linux", "Darwin"]:  # Unix-like systems (Linux, macOS)
        try:
            result = subprocess.run(["ls", "-lO", filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode("utf-8")
            # Check if the output contains 'hidden' attribute
            if "hidden" in output:
                return True
        except Exception as e:
            print(f"Error checking hidden attribute for {filepath}: {e}")
    
    return False

def get_file_info(filepath):
    """Gets file information: path, size, creation time, modification time."""
    stats = os.stat(filepath)
    return {
        "path": filepath,
        "size": stats.st_size,
        "created": datetime.datetime.fromtimestamp(stats.st_ctime),
        "modified": datetime.datetime.fromtimestamp(stats.st_mtime),
    }

def find_duplicate_files(specific_ext=None, excluded_dirs=None):
    """Finds files with the same name and type, grouped by name, excluding hidden files and specified directories."""
    if excluded_dirs is None:
        excluded_dirs = []

    file_groups = {}
    for root, _, files in os.walk("."):
        # Ensure both root and excluded_dirs are absolute paths
        abs_root = os.path.abspath(root)
        if any(abs_root.startswith(os.path.abspath(excluded)) for excluded in excluded_dirs):
            continue  # Skip this directory

        for filename in files:
            filepath = os.path.join(root, filename)
            if is_hidden(filepath):
                continue  # Skip hidden files
            name, ext = os.path.splitext(filename)
            if specific_ext and ext.lower() != specific_ext.lower():
                continue  # Skip files that do not match the specific extension
            if name not in file_groups:
                file_groups[name] = []
            file_groups[name].append(filepath)

    duplicates = {name: paths for name, paths in file_groups.items() if len(paths) > 1}
    return duplicates

def compare_and_delete(duplicates):
    """Compares files and prompts the user for deletion."""
    for name, paths in duplicates.items():
        print(f"\nDuplicate files found for '{name}':")
        for i, path in enumerate(paths):
            info = get_file_info(path)
            print(f"  [{i}] {path}")
            print(f"      Size: {info['size']} bytes")
            print(f"      Created: {info['created']}")
            print(f"      Modified: {info['modified']}")

        choice = input("Enter the numbers of files to delete (comma-separated, or 'skip'): ")
        if choice.lower() == "skip":
            continue

        try:
            indices_to_delete = [int(idx.strip()) for idx in choice.split(",")]
            for idx in indices_to_delete:
                if 0 <= idx < len(paths):
                    file_to_delete = paths[idx]
                    os.remove(file_to_delete)
                    print(f"  Deleted: {file_to_delete}")
                else:
                    print(f"  Invalid index: {idx}")
        except ValueError:
            print("  Invalid input. Please enter numbers or 'skip'.")

if __name__ == "__main__":
    # Prompt for directories to exclude
    exclude_dirs = input("Do you want to exclude any directories? (yes/no): ").strip().lower()
    excluded_dirs = []
    
    if exclude_dirs == "yes":
        print("Enter the full paths of directories to exclude (comma-separated):")
        excluded_input = input().strip()
        excluded_dirs = [dir.strip() for dir in excluded_input.split(",") if dir.strip()]

    # Ask user if they want to search by a specific file type
    filter_by_ext = input("Do you want to find duplicates for a specific file type? (yes/no): ").strip().lower()
    
    specific_ext = None
    if filter_by_ext == "yes":
        specific_ext = input("Enter the file extension (e.g., '.txt', '.jpg', '.pdf'): ").strip().lower()
        if not specific_ext.startswith("."):
            specific_ext = "." + specific_ext  # Ensure the extension starts with a dot
    
    duplicates = find_duplicate_files(specific_ext, excluded_dirs)
    
    if duplicates:
        compare_and_delete(duplicates)
    else:
        print("No duplicate files found.")
