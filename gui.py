import tkinter as tk
from tkinter import ttk, messagebox
from vehicle import Vehicle
from main import Problem
from solver import bfs, dfs, ucs, a_star  # Tất cả solver trong 1 file

CELL_SIZE = 80
GRID_SIZE = 6

class RushHourGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rush Hour Solver")
        self.canvas = tk.Canvas(root, width=CELL_SIZE*GRID_SIZE, height=CELL_SIZE*GRID_SIZE)
        self.canvas.grid(row=0, column=0, columnspan=4)

        self.algorithm = tk.StringVar(value='UCS')
        self.playing = False
        self.current_step = 0
        self.solution = []

        tk.Label(root, text="Algorithm:").grid(row=1, column=0)
        algo_menu = ttk.Combobox(root, textvariable=self.algorithm, values=['UCS', 'BFS', 'DFS', 'A*'], state="readonly")
        algo_menu.grid(row=1, column=1)

        tk.Button(root, text="Solve", command=self.solve).grid(row=1, column=2)
        tk.Button(root, text="Play", command=self.play).grid(row=1, column=3)
        tk.Button(root, text="Pause", command=self.pause).grid(row=2, column=0)
        tk.Button(root, text="Reset", command=self.reset).grid(row=2, column=1)

        self.stats_label = tk.Label(root, text="Steps: 0 | Cost: 0")
        self.stats_label.grid(row=2, column=2, columnspan=2)

        self.init_game()

    def init_game(self):
        self.vehicles = {
            Vehicle('X', 1, 2, 'H'),
            Vehicle('A', 0, 0, 'V'),
            Vehicle('B', 3, 0, 'V'),
            Vehicle('C', 5, 0, 'V'),
            Vehicle('D', 0, 3, 'H'),
            Vehicle('E', 4, 3, 'V'),
            Vehicle('F', 2, 5, 'H'),
        }
        self.problem = Problem(self.vehicles)
        self.draw_board(self.problem)

    def draw_board(self, problem):
        board = problem.get_board()
        self.canvas.delete("all")
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                cell = board[y][x]
                if cell != ' ':
                    color = 'red' if cell == 'X' else 'skyblue'
                    x0, y0 = x * CELL_SIZE, y * CELL_SIZE
                    x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black", width=2)
                    self.canvas.create_text((x0+x1)//2, (y0+y1)//2, text=cell, font=("Arial", 14, "bold"))

    def solve(self):
        algo = self.algorithm.get()
        if algo == 'UCS':
            result = ucs(self.problem)
        elif algo == 'BFS':
            result = bfs(self.problem)
        elif algo == 'DFS':
            result = dfs(self.problem)
        elif algo == 'A*':
            result = a_star(self.problem)
        else:
            messagebox.showerror("Error", "Unknown algorithm selected.")
            return

        if not result['solutions']:
            messagebox.showinfo("No solution", "Không tìm thấy lời giải.")
            return

        self.solution = result['solutions'][0]
        self.current_step = 0
        self.stats_label.config(
            text=f"Steps: {len(self.solution) - 1} | Cost: {self.calculate_cost(self.solution)}"
        )
        self.draw_board(self.solution[0])

    def calculate_cost(self, solution):
        cost = 0
        for i in range(len(solution) - 1):
            moved = list(solution[i].vehicles - solution[i + 1].vehicles)[0]
            cost += moved.length
        return cost

    def play(self):
        if not self.solution:
            return
        self.playing = True
        self.animate()

    def pause(self):
        self.playing = False

    def reset(self):
        self.playing = False
        self.current_step = 0
        self.solution = []
        self.stats_label.config(text="Steps: 0 | Cost: 0")
        self.draw_board(self.problem)

    def animate(self):
        if self.playing and self.current_step < len(self.solution):
            self.draw_board(self.solution[self.current_step])
            self.current_step += 1
            self.root.after(500, self.animate)
        elif self.current_step >= len(self.solution):
            self.playing = False
            messagebox.showinfo("Done", "Hoàn tất lời giải.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RushHourGUI(root)
    root.mainloop()
