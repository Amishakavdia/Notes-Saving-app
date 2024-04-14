#it is a built-in Python module that provides a  way to create GUI applications.
# It is based on the Tk GUI toolkit, which is popular for its simplicity and ease of use.

import tkinter as tk

#ttk stands for themed tkinter.
# It's an additional module
# provides themed widgets that have a more modern and native appearance compared to the standard tkinter widgets.
#For example, ttk.Button, ttk.Label, ttk.Entry, etc.
#Message boxes are used to display informational messages, warnings, errors, and ask for confirmation from the user.

from tkinter import ttk, messagebox

# json module is part of the standard library
# It provides functionality to encode Python objects into JSON format (serialization)
# and decode JSON data back into Python objects (deserialization).

import json

#The ttkbootstrap package is a third-party library that provides Bootstrap-themed styles for tkinter widgets in Python.
#you can create an instance of the Style class and use it to apply Bootstrap-themed styles to your tkinter widgets

from ttkbootstrap import Style


# Creating the main window by providing title , geometry and style.

root = tk.Tk()
root.title("Notes App")
root.geometry("500x500")
style = Style(theme='journal')
style = ttk.Style()

# Configuring the tab font to be bold

style.configure("TNotebook.Tab", font=("TkDefaultFont", 14, "bold"))

# Creating the notebook to hold the notes

notebook = ttk.Notebook(root, style="TNotebook")

# Load saved notes
notes = {}
try:
    with open("notes.json", "r") as f:
        notes = json.load(f)
except FileNotFoundError:
    pass

# Create the notebook to hold the notes
notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


# Create a function to add a new note
def add_note():
    # Create a new tab for the note
    note_frame = ttk.Frame(notebook, padding=10)
    notebook.add(note_frame, text="New Note")

    # Create entry widgets for the title and content of the note
    title_label = ttk.Label(note_frame, text="Title:")
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")

    title_entry = ttk.Entry(note_frame, width=40)
    title_entry.grid(row=0, column=1, padx=10, pady=10)

    content_label = ttk.Label(note_frame, text="Content:")
    content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

    content_entry = tk.Text(note_frame, width=40, height=10)
    content_entry.grid(row=1, column=1, padx=10, pady=10)

    # Create a function to save the note
    def save_note():
        # Get the title and content of the note
        title = title_entry.get()
        content = content_entry.get("1.0", tk.END)

        # Add the note to the notes dictionary
        notes[title] = content.strip()

        # Save the notes dictionary to the file
        with open("notes.json", "w") as f:
            json.dump(notes, f)

        # Add the note to the notebook
        note_content = tk.Text(notebook, width=40, height=10)
        note_content.insert(tk.END, content)
        notebook.forget(notebook.select())
        notebook.add(note_content, text=title)

    # Add a save button to the note frame
    save_button = ttk.Button(note_frame, text="Save",
                             command=save_note, style="secondary.TButton")
    save_button.grid(row=2, column=1, padx=10, pady=10)


def load_notes():
    try:
        with open("notes.json", "r") as f:
            notes = json.load(f)

        for title, content in notes.items():
            # Add the note to the notebook
            note_content = tk.Text(notebook, width=40, height=10)
            note_content.insert(tk.END, content)
            notebook.add(note_content, text=title)

    except FileNotFoundError:
        # If the file does not exist, do nothing
        pass


# Call the load_notes function when the app starts
load_notes()


# Create a function to delete a note
def delete_note():
    # Get the current tab index
    current_tab = notebook.index(notebook.select())

    # Get the title of the note to be deleted
    note_title = notebook.tab(current_tab, "text")

    # Show a confirmation dialog
    confirm = messagebox.askyesno("Delete Note",
                                  f"Are you sure you want to delete {note_title}?")

    if confirm:
        # Remove the note from the notebook
        notebook.forget(current_tab)

        # Remove the note from the notes dictionary
        notes.pop(note_title)

        # Save the notes dictionary to the file
        with open("notes.json", "w") as f:
            json.dump(notes, f)


# Add buttons to the main window
new_button = (ttk.Button(root, text="New Note",
                        command=add_note, style="info.TButton"))
new_button.pack(side=tk.LEFT, padx=10, pady=10)

delete_button = ttk.Button(root, text="Delete",
                           command=delete_note, style="primary.TButton")
delete_button.pack(side=tk.LEFT, padx=10, pady=10)

# root.mainloop() is a method that starts the event loop of the application.
# The event loop is an infinite loop that waits for events to occur and then processes them.
# These events can include user interactions such as button clicks, key presses, mouse movements, etc.

root.mainloop()
