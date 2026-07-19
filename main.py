"""
main.py

Simple Tkinter GUI for organizing files in a chosen folder by type.
"""

import tkinter as tk
from tkinter import filedialog, messagebox

from organizer import organize_folder

WINDOW_TITLE = "File Organizer"
WINDOW_SIZE = "600x450"

"""comments for test in git"""
def browse_folder() -> None:
    """Prompt the user for a folder, organize it, and display the results."""
    folder = filedialog.askdirectory()
    if not folder:
        return

    try:
        moved, stats, total = organize_folder(folder)
    except Exception as error:
        messagebox.showerror("Error", str(error))
        return

    display_results(moved, stats, total)
    messagebox.showinfo("Success", "Files organized successfully!")


def display_results(moved: list, stats: dict, total: int) -> None:
    """Render the organization results in the output text box."""
    output.delete(1.0, tk.END)

    if not moved:
        output.insert(tk.END, "No files found.")
        return

    output.insert(tk.END, "Moved Files\n")
    output.insert(tk.END, "-" * 40 + "\n\n")
    for file_description in moved:
        output.insert(tk.END, file_description + "\n")

    output.insert(tk.END, "\n" + "=" * 40 + "\n")
    output.insert(tk.END, "Organization Summary\n")
    output.insert(tk.END, "=" * 40 + "\n\n")
    output.insert(tk.END, f"Total Files : {total}\n\n")

    for category, count in stats.items():
        output.insert(tk.END, f"{category}: {count}\n")


def build_gui() -> tk.Tk:
    """Construct and return the main application window."""
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.geometry(WINDOW_SIZE)

    title_label = tk.Label(
        root,
        text="Python File Organizer",
        font=("Arial", 18, "bold"),
    )
    title_label.pack(pady=15)

    choose_button = tk.Button(
        root,
        text="Choose Folder",
        font=("Arial", 12),
        command=browse_folder,
    )
    choose_button.pack()

    global output
    output = tk.Text(root, width=70, height=18)
    output.pack(pady=20)

    return root


if __name__ == "__main__":
    app = build_gui()
    app.mainloop()