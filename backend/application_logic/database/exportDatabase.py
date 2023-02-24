import tkinter as tk
from tkinter import filedialog

from databaseQueries import *

# Opens file dialog and prints there all the data stored in the database
root = tk.Tk()
root.withdraw()

try:
    file_path = filedialog.asksaveasfile(filetypes=(("Text files", "*.txt"), ("All files", "*.*"))).name

    while (file_path.endswith(".txt")):
        file_path = file_path[:-4]

    count = 0
    with open(file_path + ".txt", 'w') as f:
        for x in get_all_entries_from_db():
            f.write(str(x) + "\n")
            count = count + 1
        f.close()

    print("Sucesfully exported " + str(count) + " entries.")
    print("Path: " + file_path + ".txt")

except Exception as e:
    print("Error creating file:")
    print(e)
