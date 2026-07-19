"""
organizer.py

Organizes files in a folder into category subfolders based on file extension.
"""

import shutil
from pathlib import Path
from typing import Dict, List, Tuple

# Maps category name -> set of file extensions (lowercase, with leading dot)
CATEGORIES: Dict[str, set] = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"},
    "Spreadsheets": {".xls", ".xlsx", ".csv", ".ods"},
    "Presentations": {".ppt", ".pptx", ".odp"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg"},
    "Video": {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".tgz"},
    "Code": {".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".json", ".xml"},
    "Executables": {".exe", ".msi", ".dmg", ".app"},
}

OTHER_CATEGORY = "Other"


def _category_for_extension(extension: str) -> str:
    """Return the category name for a given file extension."""
    extension = extension.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return OTHER_CATEGORY


def organize_folder(folder: str) -> Tuple[List[str], Dict[str, int], int]:
    """
    Organize all files directly inside `folder` into category subfolders.

    Files are moved into subfolders (created if needed) named after their
    category, e.g. "Images", "Documents", "Other".

    Args:
        folder: Path to the folder to organize.

    Returns:
        A tuple of:
            moved: list of strings describing each moved file,
                   e.g. "photo.jpg -> Images"
            stats: dict mapping category name -> number of files moved there
            total: total number of files moved
    """
    folder_path = Path(folder)

    if not folder_path.is_dir():
        raise ValueError(f"'{folder}' is not a valid folder.")

    moved: List[str] = []
    stats: Dict[str, int] = {}

    # Only look at files directly in the folder (skip subfolders already there)
    files = [f for f in folder_path.iterdir() if f.is_file()]

    for file_path in files:
        category = _category_for_extension(file_path.suffix)
        destination_folder = folder_path / category
        destination_folder.mkdir(exist_ok=True)

        destination_path = destination_folder / file_path.name

        # Avoid overwriting a file that already exists at the destination
        destination_path = _get_unique_destination(destination_path)

        shutil.move(str(file_path), str(destination_path))

        moved.append(f"{file_path.name} -> {category}")
        stats[category] = stats.get(category, 0) + 1

    total = len(moved)
    return moved, stats, total


def _get_unique_destination(destination_path: Path) -> Path:
    """If destination_path already exists, append a number to keep it unique."""
    if not destination_path.exists():
        return destination_path

    stem = destination_path.stem
    suffix = destination_path.suffix
    parent = destination_path.parent

    counter = 1
    new_path = parent / f"{stem} ({counter}){suffix}"
    while new_path.exists():
        counter += 1
        new_path = parent / f"{stem} ({counter}){suffix}"

    return new_path