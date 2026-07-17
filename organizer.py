import os
import shutil


def organize_folder(folder):
    categories = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
        "Documents": [".pdf", ".docx", ".doc", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"],
        "Music": [".mp3", ".wav", ".aac"],
        "Videos": [".mp4", ".avi", ".mkv", ".mov"],
        "Python Files": [".py"]
    }

    # Create folders
    for category in categories:
        os.makedirs(os.path.join(folder, category), exist_ok=True)

    os.makedirs(os.path.join(folder, "Others"), exist_ok=True)

    moved_files = []

    for file in os.listdir(folder):

        source = os.path.join(folder, file)

        if os.path.isdir(source):
            continue

        extension = os.path.splitext(file)[1].lower()

        moved = False

        for category, extensions in categories.items():

            if extension in extensions:

                destination = os.path.join(folder, category, file)

                shutil.move(source, destination)

                moved_files.append(f"{file} ➜ {category}")

                moved = True

                break

        if not moved:

            destination = os.path.join(folder, "Others", file)

            shutil.move(source, destination)

            moved_files.append(f"{file} ➜ Others")

    return moved_files