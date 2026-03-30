import os
import hashlib
import shutil

def hash_file(path):
    """Return SHA256 hash of a file."""
    sha = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                sha.update(chunk)
    except Exception as e:
        print(f"Cannot read {path}: {e}")
        return None
    return sha.hexdigest()

def find_and_move_duplicates_recursive(root_folder, duplicate_folder):
    """Recursively scan folder and move duplicates to duplicate_folder."""
    
    if not os.path.exists(duplicate_folder):
        os.makedirs(duplicate_folder)

    hashes = {}  # Store seen file hashes
    duplicates = []

    for dirpath, _, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(dirpath, file)
            file_hash = hash_file(file_path)
            if not file_hash:
                continue
            if file_hash in hashes:
                # Duplicate found, move to duplicate folder
                duplicates.append(file_path)
                dest_path = os.path.join(duplicate_folder, os.path.basename(file_path))
                counter = 1
                # Avoid overwriting
                while os.path.exists(dest_path):
                    name, ext = os.path.splitext(file)
                    dest_path = os.path.join(duplicate_folder, f"{name}_{counter}{ext}")
                    counter += 1
                shutil.move(file_path, dest_path)
                print(f"Moved duplicate: {file_path} --> {dest_path}")
            else:
                hashes[file_hash] = file_path

    print(f"\nScan complete. Total duplicates moved: {len(duplicates)}")
    print(f"All duplicates are now in: {duplicate_folder}")

# ------------------ Usage ------------------
root_folder = r"D:\PHOTOS_DATA"                  # Your external drive folder
duplicate_folder = r"D:\PHOTOS_DATA\Duplicates"  # Central folder for duplicates

find_and_move_duplicates_recursive(root_folder, duplicate_folder)