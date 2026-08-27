import os
import re

def ensure_directory_exists(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def get_file_extension(file_path: str) -> str:
    return os.path.splitext(file_path)[1].lower()

def list_files_in_directory(directory: str, extensions: list = None) -> list:
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if extensions and get_file_extension(filename) not in extensions:
                continue
            files.append(os.path.join(root, filename))
    return files