import pygame
import os
from vehicle import Vehicle
from main import Problem
from solver import bfs, dfs, ucs, a_star_solver
import time

# Constants
CELL_SIZE = 80
GRID_SIZE = 6
SCREEN_WIDTH = CELL_SIZE * GRID_SIZE
SCREEN_HEIGHT = CELL_SIZE * GRID_SIZE + 80

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
BLUE = (100, 180, 255)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rush Hour Solver (Pygame)")
font = pygame.font.SysFont("Arial", 20)

clock = pygame.time.Clock()

class GUI:
    def __init__(self):
        self.problem = None
        self.solution = []
        self.current_step = 0
        self.playing = False
        self.vehicles = set()

        self.selected_map = None
        self.algorithm = 'UCS'

    def load_map(self, filename):
        self.vehicles = set()
        with open(os.path.join("Map", filename), "r") as file:
            for line in file:
                line = line.strip()
                if len(line) != 4:
                    continue
                vid = line[0]
                row = int(line[1])
                col = int(line[2])
                orient = line[3]
                self.vehicles.add(Vehicle(vid, col, row, orient))
        self.problem = Problem(self.vehicles)
        self.solution = []
        self.current_step = 0

    def draw_board(self, problem):
        screen.fill(WHITE)
        board = problem.get_board()
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLACK, rect, 1)
                cell = board[y][x]
                if cell != ' ':
                    color = RED if cell == 'X' else BLUE
                    pygame.draw.rect(screen, color, rect)
                    text = font.render(cell, True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

        # Draw info
        pygame.draw.rect(screen, (230, 230, 230), (0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80))
        info = f"Map: {self.selected_map or 'None'} | Algorithm: {self.algorithm} | Step: {self.current_step}/{len(self.solution)-1 if self.solution else 0}"
        cost_text = font.render(info, True, BLACK)
        screen.blit(cost_text, (10, SCREEN_HEIGHT - 70))

        if self.solution:
            cost = self.calculate_cost(self.solution)
            cost_label = font.render(f"Total Cost: {cost}", True, BLACK)
            screen.blit(cost_label, (10, SCREEN_HEIGHT - 40))

    def solve(self):
        if not self.problem:
            return
        if self.algorithm == 'UCS':
            result = ucs(self.problem)
        elif self.algorithm == 'BFS':
            result = bfs(self.problem)
        elif self.algorithm == 'DFS':
            result = dfs(self.problem)
        elif self.algorithm == 'A*':
            result = a_star_solver(self.problem)
        else:
            return
        if not result['solutions']:
            print("No solution found.")
            return
        self.solution = result['solutions'][0]
        self.current_step = 0

    def calculate_cost(self, solution):
        cost = 0
        for i in range(len(solution) - 1):
            moved = list(solution[i].vehicles - solution[i + 1].vehicles)[0]
            cost += moved.length
        return cost

    def animate(self):
        if self.playing and self.solution and self.current_step < len(self.solution):
            self.draw_board(self.solution[self.current_step])
            pygame.display.flip()
            self.current_step += 1
            time.sleep(0.5)
        elif self.current_step >= len(self.solution):
            self.playing = False

def run():
    gui = GUI()

    # Select map file from list
    maps = [f for f in os.listdir("Map") if f.endswith(".txt")]
    print("Available maps:")
    for idx, name in enumerate(maps):
        print(f"{idx + 1}. {name}")
    map_idx = int(input("Select map number: ")) - 1
    gui.selected_map = maps[map_idx]
    gui.load_map(gui.selected_map)

    # Select algorithm
    algo = input("Select algorithm [UCS, BFS, DFS, A*]: ").strip().upper()
    if algo in ['UCS', 'BFS', 'DFS', 'A*']:
        gui.algorithm = algo
    else:
        gui.algorithm = 'UCS'

    gui.draw_board(gui.problem)
    pygame.display.flip()

    # Main loop
    running = True
    while running:
        gui.draw_board(gui.solution[gui.current_step] if gui.solution else gui.problem)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:      # Play/Pause
                    gui.playing = not gui.playing
                elif event.key == pygame.K_r:        # Reset
                    gui.current_step = 0
                    gui.playing = False
                elif event.key == pygame.K_s:        # Solve
                    gui.solve()
                elif event.key == pygame.K_RIGHT:    # Step forward
                    if gui.solution and gui.current_step < len(gui.solution) - 1:
                        gui.current_step += 1
                elif event.key == pygame.K_LEFT:     # Step backward
                    if gui.solution and gui.current_step > 0:
                        gui.current_step -= 1

        if gui.playing:
            gui.animate()

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    run()
