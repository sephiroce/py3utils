import os
import hashlib
from collections import defaultdict

def get_file_hash(file_path, chunk_size=8192):
    """Calculate SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (OSError, IOError):
        return None

def find_duplicate_files(directory):
    """Find and print duplicate files in a directory recursively."""
    hash_map = defaultdict(list)
    
    file_idx = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_idx += 1
            if file_idx % 1000 == 0:
              print("%d files were processed"%file_idx)
            file_path = os.path.join(root, file)
            file_hash = get_file_hash(file_path)
            if file_hash:
                hash_map[file_hash].append(file_path)

    print("Total %d files were processed"%file_idx)
    print("Now finding duplicates")
    duplicates = {hash_val: paths for hash_val, paths in hash_map.items() if len(paths) > 1}
    
    if duplicates:
        dup_file = open("duplicated_files.list", "w")
        print("Duplicate files found:")
        for paths in duplicates.values():
            dup_file.write("\n".join(paths))
            dup_file.write("\n")
            dup_file.write("-" * 40)
            dup_file.write("\n")
            print("\n".join(paths))
            print("-" * 40)
        dup_file.close()
    else:
        print("No duplicate files found.")

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ").strip()
    if os.path.isdir(folder_path):
        find_duplicate_files(folder_path)
    else:
        print("Invalid directory path.")
