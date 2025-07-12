import pygame
import os
import time
from vehicle import Vehicle
from main import Problem
from solver import bfs, dfs, ucs, a_star_solver

pygame.init()
font = pygame.font.SysFont("Arial", 20)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Rush Hour Solver")

# Constants
CELL = 60
LEFT_MARGIN = 250
GRID_ORIGIN = (LEFT_MARGIN, 60)
WHITE = (255, 255, 255)
GRAY = (230, 230, 230)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
COLORS = [
    (255, 102, 102), (102, 255, 255), (102, 255, 102), (255, 255, 102),
    (255, 153, 255), (153, 153, 255), (255, 204, 153), (204, 255, 153),
    (204, 153, 255), (153, 255, 204), (255, 255, 153), (255, 204, 204)
]
id_colors = {}

# Game state
maps = sorted([f for f in os.listdir("Map") if f.endswith(".txt")])
solvers = ["A*", "UCS", "BFS", "DFS"]
map_idx = 0
solver_idx = 0
problem = None
solution = []
current_step = 0
playing = False
last_play_time = 0
screen_state = "home"  # Only home & play now

def draw_home_screen():
    screen.fill((240, 245, 255))  # Light background for polish

    title_font = pygame.font.SysFont("Arial", 40, bold=True)
    subtitle_font = pygame.font.SysFont("Arial", 24)

    title = title_font.render("RUSH HOUR SOLVER", True, BLACK)
    subtitle = subtitle_font.render("Escape the gridlock!", True, (80, 80, 80))

    screen.blit(title, title.get_rect(center=(400, 180)))
    screen.blit(subtitle, subtitle.get_rect(center=(400, 230)))

    # Start Button
    pygame.draw.rect(screen, (100, 200, 100), (310, 300, 180, 50), border_radius=8)
    screen.blit(font.render("Start Game", True, WHITE), (355, 315))

    # Exit Button
    pygame.draw.rect(screen, (200, 80, 80), (310, 370, 180, 50), border_radius=8)
    screen.blit(font.render("Exit (Esc)", True, WHITE), (365, 385))


def draw_board(state):
    board = state.get_board()
    for y in range(6):
        for x in range(6):
            rect = pygame.Rect(GRID_ORIGIN[0]+x*CELL, GRID_ORIGIN[1]+y*CELL, CELL, CELL)
            pygame.draw.rect(screen, (220,220,220), rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            cell = board[y][x]
            if cell != ' ':
                if cell not in id_colors:
                    color = RED if cell == 'X' else COLORS[len(id_colors)%len(COLORS)]
                    id_colors[cell] = color
                pygame.draw.rect(screen, id_colors[cell], rect)
                label = font.render(cell, True, BLACK)
                screen.blit(label, label.get_rect(center=rect.center))
    pygame.draw.polygon(screen, RED, [
        (GRID_ORIGIN[0] + 6*CELL + 10, GRID_ORIGIN[1] + 2*CELL + 20),
        (GRID_ORIGIN[0] + 6*CELL + 30, GRID_ORIGIN[1] + 2*CELL + 30),
        (GRID_ORIGIN[0] + 6*CELL + 10, GRID_ORIGIN[1] + 2*CELL + 40)
    ])
    screen.blit(font.render("EXIT", True, RED),
                (GRID_ORIGIN[0] + 6*CELL + 35, GRID_ORIGIN[1] + 2*CELL + 20))

def draw_game_ui():
    pygame.draw.rect(screen, (245, 245, 245), (20, 20, 200, 560))
    screen.blit(font.render("Rush Hour Solver", True, BLACK), (30, 30))

    # Map selector
    screen.blit(font.render("Board:", True, BLACK), (30, 70))
    pygame.draw.rect(screen, GRAY, (100, 70, 80, 25))
    pygame.draw.rect(screen, (180, 180, 180), (90, 70, 20, 25))
    pygame.draw.rect(screen, (180, 180, 180), (193, 70, 20, 25))
    screen.blit(font.render("<", True, BLACK), (95, 72))
    screen.blit(font.render(">", True, BLACK), (195, 72))
    screen.blit(font.render(maps[map_idx], True, BLACK), (110, 72))

    # Solver selector
    screen.blit(font.render("Solver:", True, BLACK), (30, 100))
    pygame.draw.rect(screen, GRAY, (110, 100, 80, 25))
    pygame.draw.rect(screen, (180, 180, 180), (90, 100, 20, 25))
    pygame.draw.rect(screen, (180, 180, 180), (193, 100, 20, 25))
    screen.blit(font.render("<", True, BLACK), (95, 102))
    screen.blit(font.render(">", True, BLACK), (195, 102))
    screen.blit(font.render(solvers[solver_idx], True, BLACK), (110, 102))
    pygame.draw.line(screen, GRAY, (30, 135), (200, 135), 2)

    # Buttons
    for i, label in enumerate(["Solve", "Play", "Reset", "Return"]):
        pygame.draw.rect(screen, (180,180,180), (50, 140 + i*60, 120, 40))
        screen.blit(font.render(label, True, BLACK), (80, 150 + i*60))

    # Solution Info
    y_base = 400
    pygame.draw.rect(screen, WHITE, (30, y_base, 160, 100))
    pygame.draw.rect(screen, BLACK, (30, y_base, 160, 100), 1)

    if solution:
        step_text = f"Step: {current_step}/{len(solution)-1}"
        current_cost = sum(list(solution[i].vehicles - solution[i+1].vehicles)[0].length for i in range(current_step))
        total_cost = sum(list(solution[i].vehicles - solution[i+1].vehicles)[0].length for i in range(len(solution)-1))
        screen.blit(font.render("Solution Info:", True, BLACK), (40, y_base + 5))
        screen.blit(font.render(step_text, True, BLACK), (40, y_base + 25))
        screen.blit(font.render(f"Current Cost: {current_cost}", True, BLACK), (40, y_base + 45))
        screen.blit(font.render(f"Total Cost: {total_cost}", True, BLACK), (40, y_base + 65))

        # Enlarged bottom message box
        pygame.draw.rect(screen, WHITE, (30, y_base + 110, 160, 60))
        pygame.draw.rect(screen, BLACK, (30, y_base + 110, 160, 60), 1)
        screen.blit(font.render(f"Solution found", True, BLACK), (40, y_base + 120))
        screen.blit(font.render(f"in {len(solution)-1} moves.", True, BLACK), (40, y_base + 140))

def load_map(filename):
    vehicles = set()
    with open(os.path.join("Map", filename)) as file:
        for i, line in enumerate(file, 1):
            line = line.strip()
            if len(line) != 4:
                continue
            vid, y, x, o = line[0], int(line[1]), int(line[2]), line[3]
            try:
                vehicles.add(Vehicle(vid, y, x, o))
            except ValueError as e:
                print(f"❌ Invalid vehicle at line {i} → {line}: {e}")
                raise
    return Problem(vehicles)

def solve():
    global solution, current_step
    algo = solvers[solver_idx]
    if algo == "A*":
        result = a_star_solver(problem)
    elif algo == "UCS":
        result = ucs(problem)
    elif algo == "BFS":
        result = bfs(problem)
    elif algo == "DFS":
        result = dfs(problem)
    solution = result['solutions'][0] if result['solutions'] else []
    current_step = 0

# Main loop
running = True
screen_state = "home"
problem = load_map(maps[map_idx])

while running:
    screen.fill((180, 220, 180))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif screen_state == "home" and event.key == pygame.K_RETURN:
                screen_state = "play"
                problem = load_map(maps[map_idx])
                solution = []
                current_step = 0
                playing = False
            elif screen_state == "play":
                if event.key == pygame.K_RIGHT and solution:
                    current_step = min(current_step + 1, len(solution) - 1)
                elif event.key == pygame.K_LEFT and solution:
                    current_step = max(current_step - 1, 0)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if screen_state == "home":
                if 310 <= x <= 490 and 300 <= y <= 350:
                    screen_state = "play"
                    problem = load_map(maps[map_idx])
                    solution = []
                    current_step = 0
                    playing = False
                elif 310 <= x <= 490 and 370 <= y <= 420:
                    running = False
            elif screen_state == "play":
                # Map/Solver arrows
                if 90 <= x <= 110:
                    if 70 <= y <= 95:  # Map <
                        map_idx = (map_idx - 1) % len(maps)
                        problem = load_map(maps[map_idx])
                        solution = []
                        current_step = 0
                    elif 100 <= y <= 125:  # Solver <
                        solver_idx = (solver_idx - 1) % len(solvers)
                elif 193 <= x <= 213:
                    if 70 <= y <= 95:  # Map >
                        map_idx = (map_idx + 1) % len(maps)
                        problem = load_map(maps[map_idx])
                        solution = []
                        current_step = 0
                    elif 100 <= y <= 125:  # Solver >
                        solver_idx = (solver_idx + 1) % len(solvers)

                # Buttons: Solve / Play / Reset / Return
                if 50 <= x <= 170:
                    if 140 <= y <= 180:  # Solve
                        solve()
                    elif 200 <= y <= 240:  # Play
                        playing = not playing
                    elif 260 <= y <= 300:  # Reset
                        current_step = 0
                        playing = False
                    elif 320 <= y <= 360:  # Return to home
                        screen_state = "home"
                        playing = False
                        current_step = 0
                        solution = []


    if screen_state == "home":
        draw_home_screen()
    elif screen_state == "play":
        draw_game_ui()
        if solution:
            draw_board(solution[current_step])
        else:
            draw_board(problem)
        if playing and solution and time.time() - last_play_time > 0.5:
            if current_step < len(solution) - 1:
                current_step += 1
            last_play_time = time.time()

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
