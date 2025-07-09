import tkinter as tk
from tkinter import messagebox
from vehicle import Vehicle
from main import Problem  
from solver import ucs  

CELL_SIZE = 80
GRID_SIZE = 6

class RushHourGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rush Hour Solver")
        self.canvas = tk.Canvas(root, width=CELL_SIZE*GRID_SIZE, height=CELL_SIZE*GRID_SIZE)
        self.canvas.grid(row=0, column=0, columnspan=4)

        self.playing = False
        self.current_step = 0
        self.solution = []

        # Buttons
        tk.Button(root, text="Solve (UCS)", command=self.solve).grid(row=1, column=0)
        tk.Button(root, text="Play", command=self.play).grid(row=1, column=1)
        tk.Button(root, text="Pause", command=self.pause).grid(row=1, column=2)
        tk.Button(root, text="Reset", command=self.reset).grid(row=1, column=3)

        # Stats
        self.stats_label = tk.Label(root, text="Steps: 0 | Cost: 0")
        self.stats_label.grid(row=2, column=0, columnspan=4)

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
        for y in range(GR
