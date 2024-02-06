import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from subprocess import call

def run_ver_1():
    call(["python", "ver-1.py"])

def run_sudoku_main():
    call(["python", "sudukoMain.py"])

def run_sel():
    call(["python", "sel.py"])

def run_main():
    call(["python", "main.py"])

# Create the main window
root = tk.Tk()
root.title("Sudoku Solver Home Page")

# Increase window size
root.geometry("500x400")

# Set background image
bg_image = Image.open("Resources/bg.png")
bg_image = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Create a style for ttk buttons
style = ttk.Style()
style.configure("TButton", padding=(9, 5), font='calibri', background='#d17a1d', foreground='black')

# Create buttons with ttk style
manual_button = ttk.Button(root, text="Manual", command=run_ver_1)
image_button = ttk.Button(root, text="Image", command=run_sudoku_main)
sel_button = ttk.Button(root, text="Website", command=run_sel)
video_button = ttk.Button(root, text="Video", command=run_main)

# Organize buttons into two columns
manual_button.grid(row=0, column=0, padx=65, pady=25)
image_button.grid(row=1, column=0, padx=65, pady=25)
sel_button.grid(row=0, column=1, padx=20, pady=25)
video_button.grid(row=1, column=1, padx=20, pady=25)

# Start the main loop
root.mainloop()
