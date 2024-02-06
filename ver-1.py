import tkinter as tk
from bs4 import BeautifulSoup
import requests
from tkinter import messagebox

def extract():
    url = 'https://five.websudoku.com/'
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    grid = []
    for i in range(9):
        grid.append([])
        for j in range(9):
            cell_value = soup.find(id='f%s%s' % (i, j)).get('value')
            grid[i].append(int(cell_value) if cell_value else 0)
    return grid

def solve(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                for k in range(1, 10):
                    if check(grid, i, j, k):
                        grid[i][j] = k
                        result = solve(grid)
                        if result:  # Check if a solution is found
                            return result
                        grid[i][j] = 0
                return None  # No solution found for this choice
    return [row[:] for row in grid]

def check(grid, i, j, k):
    for x in range(9):
        if grid[i][x] == k:
            return False
    for y in range(9):
        if grid[y][j] == k:
            return False
    for x in range(3):
        for y in range(3):
            if grid[(i // 3) * 3 + x][(j // 3) * 3 + y] == k:
                return False
    return True

class SudokuGUI(tk.Tk):
    def __init__(self, initial_grid):
        tk.Tk.__init__(self)
        self.title("Sudoku Solver")
        self.grid_values = [[tk.StringVar() for j in range(9)] for i in range(9)]
        self.create_grid(initial_grid)
        self.create_buttons()

    def create_grid(self, initial_grid):
        for i in range(9):
            for j in range(9):
                frame = tk.Frame(self, relief='ridge', borderwidth=2)
                frame.grid(row=i, column=j, sticky='nsew')
                if initial_grid[i][j] != 0:
                    label = tk.Label(frame, text=str(initial_grid[i][j]), font=('Helvetica', 16, 'bold'),
                                     width=4, height=2)
                    label.pack(fill='both', expand=True)
                else:
                    entry = tk.Entry(frame, textvariable=self.grid_values[i][j], font=('Helvetica', 16),
                                     width=4, justify='center')
                    entry.pack(fill='both', expand=True)

        # Add black thicker lines after every 3 rows and columns
        for i in range(3, 10, 3):
            self.grid_columnconfigure(i, minsize=2)
            self.grid_rowconfigure(i, minsize=2)
        
        
        

    def create_buttons(self):
        check_button = tk.Button(self, text="Check", command=self.check_solution)
        check_button.grid(row=9, column=3, pady=10, padx=5)

        solve_button = tk.Button(self, text="Solve", command=self.solve_sudoku)
        solve_button.grid(row=9, column=5, pady=10, padx=5)

    def check_solution(self):
        user_solution = [[int(self.grid_values[i][j].get()) if self.grid_values[i][j].get().strip() else 0 for j in
                          range(9)] for i in range(9)]

        # Check if any field is left blank
        if any(0 in row for row in user_solution):
            messagebox.showinfo("Check Result", "Please fill in all fields to check the solution.")
            return

        initial_grid = [[grid[i][j] for j in range(9)] for i in range(9)]
        solved_user_solution = solve(user_solution)
        solved_grid1 = solve(initial_grid)
        if solved_user_solution is not None and solved_user_solution == solved_grid1:
            messagebox.showinfo("Check Result", "Correct solution!")
        else:
            messagebox.showinfo("Check Result", "Incorrect solution!")

    def solve_sudoku(self):
        initial_grid = [[grid[i][j] for j in range(9)] for i in range(9)]
        user_input = [[int(self.grid_values[i][j].get()) if self.grid_values[i][j].get() else 0 for j in range(9)] for
                      i in range(9)]
        solved_grid = solve(initial_grid)

        for i in range(9):
            for j in range(9):
                self.grid_values[i][j].set(solved_grid[i][j])


grid = extract()
app = SudokuGUI(grid)
app.mainloop()
