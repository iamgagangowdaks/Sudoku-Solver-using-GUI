import tkinter as tk
from tkinter import messagebox

def solve_sudoku(board):
    if not find_empty_cell(board):
        return True
    
    row, col = find_empty_cell(board)
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def find_empty_cell(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None

def is_valid(board, row, col, num):
    # Check row
    if num in board[row]:
        return False
    
    # Check column
    if num in [board[i][col] for i in range(9)]:
        return False
    
    # Check 3x3 box
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_button_click():
    # Get the board values from entry widgets
    board = []
    for i in range(9):
        row = []
        for j in range(9):
            entry = entry_widgets[i][j].get()
            if entry == "":
                row.append(0)
            else:
                try:
                    num = int(entry)
                    if 1 <= num <= 9:
                        row.append(num)
                    else:
                        messagebox.showwarning("Invalid Input", "Please enter a digit between 1 and 9.")
                        return
                except ValueError:
                    messagebox.showwarning("Invalid Input", "Please enter a valid integer between 1 and 9.")
                    return
        board.append(row)
    
    # Validate input
    if not is_valid_input(board):
        return
    
    # Highlight wrong entries
    highlight_wrong_entries(board)
    
    # Solve the Sudoku
    if solve_sudoku(board):
        # Update the entry widgets with the solved values
        for i in range(9):
            for j in range(9):
                entry_widgets[i][j].delete(0, tk.END)
                entry_widgets[i][j].insert(0, str(board[i][j]))
                entry_widgets[i][j].config(bg=block_colors[i//3][j//3])  # Reset background color
    else:
        messagebox.showwarning("No Solution", "No solution found!")

def is_valid_input(board):
    # Check for repeating numbers in rows and columns
    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num != 0 and (board[i].count(num) > 1 or [board[x][j] for x in range(9)].count(num) > 1):
                highlight_entry(i, j)
                messagebox.showerror("Invalid Input", "Invalid Sudoku input. Please check for repeating numbers in rows and columns.")
                return False
    
    # Check for repeating numbers and 2-digit numbers in 3x3 boxes
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            box = [board[x][y] for x in range(i, i+3) for y in range(j, j+3)]
            for num in set(box):
                if num != 0 and (box.count(num) > 1 or (len(str(num)) == 2 and any(len(str(x)) == 2 for x in box))):
                    for x in range(i, i+3):
                        for y in range(j, j+3):
                            highlight_entry(x, y)
                    messagebox.showerror("Invalid Input", "Invalid Sudoku input. Please check for repeating numbers and 2-digit numbers in 3x3 boxes.")
                    return False
    
    # Reset highlighting
    for i in range(9):
        for j in range(9):
            entry_widgets[i][j].config(bg=block_colors[i//3][j//3])
    
    return True

def highlight_wrong_entries(board):
    error_detected = False
    for i in range(9):
        for j in range(9):
            if entry_widgets[i][j].get() != str(board[i][j]) and entry_widgets[i][j].get() != "":
                highlight_entry(i, j)
                error_detected = True
    
    if error_detected:
        messagebox.showerror("Wrong Entry", "Please check your input. Incorrect number detected.")

def highlight_entry(row, col):
    entry_widgets[row][col].config(bg="red")

# Create the GUI window
window = tk.Tk()
window.title("Sudoku Solver")

# Increase font size and widget size
font_size = 40
entry_width = 3

# Define colors for 3x3 blocks
block_colors = [
    ["lightblue", "lightgreen", "lightyellow"],
    ["lightgreen", "lightyellow", "lightblue"],
    ["lightyellow", "lightblue", "lightgreen"]
]

# Create the entry widgets for the Sudoku board with colors
entry_widgets = []
for i in range(9):
    row_widgets = []
    for j in range(9):
        color = block_colors[i//3][j//3]
        entry = tk.Entry(window, width=entry_width, font=("Arial", font_size), bg=color, justify="center")
        entry.grid(row=i, column=j, sticky="nsew")  # Align at the middle
        row_widgets.append(entry)
    entry_widgets.append(row_widgets)

# Create the solve button
solve_button = tk.Button(window, text="Solve", command=solve_button_click, font=("Arial", font_size))
solve_button.grid(row=9, columnspan=9, sticky="nsew")  # Align at the middle

# Set window size to be larger
window.geometry("500x500")  # You can adjust the size as needed

# Configure grid weights to make the cells expand and center in the window
for i in range(9):
    window.grid_rowconfigure(i, weight=1)
    window.grid_columnconfigure(i, weight=1)

# Start the GUI main loop
window.mainloop()
