import tkinter as tk
from tkinter import filedialog, messagebox

from organizer import organize_folder


def browse_folder():

    folder = filedialog.askdirectory()

    if not folder:
        return

    try:

        moved = organize_folder(folder)

        output.delete(1.0, tk.END)

        if moved:

            for file in moved:
                output.insert(tk.END, file + "\n")

        else:

            output.insert(tk.END, "No files found.")

        messagebox.showinfo("Success", "Files organized successfully!")

    except Exception as e:

        messagebox.showerror("Error", str(e))


root = tk.Tk()

root.title("File Organizer")

root.geometry("600x450")

title = tk.Label(root,
                 text="Python File Organizer",
                 font=("Arial", 18, "bold"))

title.pack(pady=15)

button = tk.Button(root,
                   text="Choose Folder",
                   font=("Arial", 12),
                   command=browse_folder)

button.pack()

output = tk.Text(root,
                 width=70,
                 height=18)

output.pack(pady=20)

root.mainloop()