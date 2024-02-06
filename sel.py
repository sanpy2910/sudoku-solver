from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import tkinter as tk
from tkinter import messagebox

def fill_sudoku_grid(driver, grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                cell_input = driver.find_element('css selector', f'#f{i}{j}')
                cell_input.send_keys(str(grid[i][j]))
                time.sleep(0.1)
                if i == 8 and j == 8:
                    cell_input.send_keys(Keys.ENTER)

def possible(x, y, n, grid):
    for i in range(0, 9):
        if grid[i][x] == n and i != y:
            return False

    for i in range(0, 9):
        if grid[y][i] == n and i != x:
            return False

    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for X in range(x0, x0 + 3):
        for Y in range(y0, y0 + 3):
            if grid[Y][X] == n:
                return False
    return True

def solve(grid):
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(x, y, n, grid):
                        grid[y][x] = n
                        if solve(grid):
                            return grid
                        grid[y][x] = 0
                return None
    return grid

def on_yes_click():
    fill_sudoku_grid(driver, solved_grid)
    time.sleep(5)
    messagebox.showinfo("Success", "Sudoku filled successfully!")
    root.destroy()

def on_no_click():
    messagebox.showinfo("Information", "You chose not to fill in the Sudoku.")
    root.destroy()

driver = webdriver.Firefox()
driver.get("https://five.websudoku.com/")
print("Opened Sudoku website")

grid = []
for i in range(9):
    row = []
    for j in range(9):
        cell_value = driver.find_element('css selector', f'#f{i}{j}').get_attribute('value')
        row.append(int(cell_value) if cell_value else 0)
    grid.append(row)

# Solve the Sudoku
solved_grid = solve(grid)
print("Solved grid:")
for row in solved_grid:
    print(row)


root = tk.Tk()
root.title("Sudoku Filler")

window_width = 300
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

label = tk.Label(root, text="Do you want to fill in the Sudoku?", font=("Arial", 12), bg="#F0F0F0")
label.pack(pady=10)

yes_button = tk.Button(root, text="Yes", command=on_yes_click, font=("Arial", 12), bg="#80C7E8", fg="white")
yes_button.pack(side="left", padx=10)

no_button = tk.Button(root, text="No", command=on_no_click, font=("Arial", 12), bg="#FF7F7F", fg="white")
no_button.pack(side="right", padx=10)

root.mainloop()

# Close the browser window
driver.quit()
