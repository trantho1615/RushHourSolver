import pygame
import os
import time
from vehicle import Vehicle
from problem import Problem
from solver import bfs, dfs, ucs, a_star_solver

pygame.init()
click_sound = pygame.mixer.Sound("assets/click.wav")
font = pygame.font.SysFont("Arial", 20)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Rush Hour Solver")
# Load home screen background
background_image = pygame.image.load("assets/rushhour.jpg").convert()
background_image = pygame.transform.scale(background_image, (800, 600))


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
no_solution_found = False


def draw_home_screen():
    screen.blit(background_image, (0, 0))  # Draw home screen background

    title_font = pygame.font.SysFont("Arial", 40, bold=True)
    subtitle_font = pygame.font.SysFont("Arial", 24)

    # Render title text
    title = title_font.render("RUSH HOUR SOLVER", True, BLACK)
    subtitle = subtitle_font.render("Escape the gridlock!", True, (50, 50, 50))

    # Calculate rects
    title_rect = title.get_rect(center=(400, 180))
    subtitle_rect = subtitle.get_rect(center=(400, 230))

    # Draw semi-transparent box behind title
    title_bg = pygame.Surface((title_rect.width + 40, title_rect.height + 20), pygame.SRCALPHA)
    title_bg.fill((255, 255, 255, 200))  # White box, alpha 200
    screen.blit(title_bg, title_bg.get_rect(center=title_rect.center))

    subtitle_bg = pygame.Surface((subtitle_rect.width + 30, subtitle_rect.height + 15), pygame.SRCALPHA)
    subtitle_bg.fill((255, 255, 255, 180))  # Slightly more transparent
    screen.blit(subtitle_bg, subtitle_bg.get_rect(center=subtitle_rect.center))

    # draw the text over the box
    screen.blit(title, title_rect)
    screen.blit(subtitle, subtitle_rect)


    # Start Button
    pygame.draw.rect(screen, (100, 200, 100), (310, 300, 180, 50), border_radius=8)
    screen.blit(font.render("Start Game", True, BLACK), (355, 315))

    # Exit Button
    pygame.draw.rect(screen, (200, 80, 80), (310, 370, 180, 50), border_radius=8)
    screen.blit(font.render("Exit", True, BLACK), (378, 385))


def draw_board(state):
    # Draw the background grid (6x6)
    for y in range(6):
        for x in range(6):
            cell_rect = pygame.Rect(
                GRID_ORIGIN[0] + x * CELL,
                GRID_ORIGIN[1] + y * CELL,
                CELL,
                CELL
            )
            pygame.draw.rect(screen, (220, 220, 220), cell_rect)  # Cell fill
            pygame.draw.rect(screen, BLACK, cell_rect, 1)         # Cell border

    # Draw all vehicles (one ID each, centered, rounded corners)
    drawn_ids = set()
    for vehicle in state.vehicles:
        if vehicle.id in drawn_ids:
            continue
        drawn_ids.add(vehicle.id)

        x, y = vehicle.x, vehicle.y
        width = CELL * vehicle.length if vehicle.orientation == 'H' else CELL
        height = CELL if vehicle.orientation == 'H' else CELL * vehicle.length

        vehicle_rect = pygame.Rect(
            GRID_ORIGIN[0] + x * CELL,
            GRID_ORIGIN[1] + y * CELL,
            width,
            height
        )

        # Assign color if new ID
        if vehicle.id not in id_colors:
            color = RED if vehicle.id == 'X' else COLORS[len(id_colors) % len(COLORS)]
            id_colors[vehicle.id] = color

        # Draw the vehicle with rounded corners
        pygame.draw.rect(screen, id_colors[vehicle.id], vehicle_rect, border_radius=12)
        pygame.draw.rect(screen, BLACK, vehicle_rect, width=2, border_radius=12)

        # Draw centered ID on vehicle
        label = font.render(vehicle.id, True, BLACK)
        screen.blit(label, label.get_rect(center=vehicle_rect.center))

    # Draw EXIT arrow
    exit_arrow = [
        (GRID_ORIGIN[0] + 6 * CELL + 10, GRID_ORIGIN[1] + 2 * CELL + 20),
        (GRID_ORIGIN[0] + 6 * CELL + 30, GRID_ORIGIN[1] + 2 * CELL + 30),
        (GRID_ORIGIN[0] + 6 * CELL + 10, GRID_ORIGIN[1] + 2 * CELL + 40)
    ]
    pygame.draw.polygon(screen, RED, exit_arrow)
    screen.blit(
        font.render("EXIT", True, RED),
        (GRID_ORIGIN[0] + 6 * CELL + 35, GRID_ORIGIN[1] + 2 * CELL + 20)
    )

    # Draw a gate at the right edge of row 2 (where the red car exits)
    gate_rect = pygame.Rect(
        GRID_ORIGIN[0] + 6 * CELL - 4,
        GRID_ORIGIN[1] + 2 * CELL + 4,
        8,
        CELL - 8
    )
    pygame.draw.rect(screen, (150, 0, 0), gate_rect, border_radius=3)
    pygame.draw.rect(screen, BLACK, gate_rect, 1, border_radius=3)



def draw_game_ui():
    # Sidebar background
    pygame.draw.rect(screen, (120, 189, 120), (20, 20, 200, 560))

    # Rounded title box
    title_text = font.render("Rush Hour", True, BLACK)
    title_rect = title_text.get_rect()
    title_box_width = title_rect.width + 20
    title_box_height = title_rect.height + 10

    # Center horizontally inside the left panel (20 → 220 width)
    title_box = pygame.Rect(
        20 + (200 - title_box_width) // 2,
        30,
        title_box_width,
        title_box_height
    )

    pygame.draw.rect(screen, (180, 220, 255), title_box, border_radius=10)
    pygame.draw.rect(screen, BLACK, title_box, 2, border_radius=10)
    screen.blit(title_text, title_text.get_rect(center=title_box.center))


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

    # Rounded Action Buttons (Solve, Play, Reset, Return)
    button_labels = ["Solve", "Play/Stop", "Reset", "Return"]
    button_colors = [(140, 220, 140), (140, 200, 255), (255, 200, 120), (255, 140, 140)]
    for i, label in enumerate(button_labels):
        btn_rect = pygame.Rect(50, 170 + i * 60, 120, 40)
        pygame.draw.rect(screen, button_colors[i], btn_rect, border_radius=12)
        pygame.draw.rect(screen, BLACK, btn_rect, 2, border_radius=12)
        text = font.render(label, True, BLACK)
        screen.blit(text, text.get_rect(center=btn_rect.center))

    # Solution Info Box
    y_base = 400
    pygame.draw.rect(screen, WHITE, (30, y_base, 160, 100))
    pygame.draw.rect(screen, BLACK, (30, y_base, 160, 100), 1)

    if solution:
        step_text = f"Step: {current_step}/{len(solution)-1}"
        current_cost = sum(list(solution[i].vehicles - solution[i + 1].vehicles)[0].length for i in range(current_step))
        total_cost = sum(list(solution[i].vehicles - solution[i + 1].vehicles)[0].length for i in range(len(solution) - 1))
        screen.blit(font.render("Solution Info:", True, BLACK), (40, y_base + 5))
        screen.blit(font.render(step_text, True, BLACK), (40, y_base + 25))
        screen.blit(font.render(f"Current Cost: {current_cost}", True, BLACK), (40, y_base + 45))
        screen.blit(font.render(f"Total Cost: {total_cost}", True, BLACK), (40, y_base + 65))

        # Result message box
        pygame.draw.rect(screen, WHITE, (30, y_base + 110, 160, 60))
        pygame.draw.rect(screen, BLACK, (30, y_base + 110, 160, 60), 1)
        screen.blit(font.render(f"Solution found", True, BLACK), (40, y_base + 120))
        screen.blit(font.render(f"in {len(solution)-1} moves.", True, BLACK), (40, y_base + 140))

    if no_solution_found:
        pygame.draw.rect(screen, (255, 240, 240), (30, 520, 160, 50), border_radius=8)
        pygame.draw.rect(screen, (200, 0, 0), (30, 520, 160, 50), width=2, border_radius=8)
        screen.blit(font.render("No solution found", True, (200, 0, 0)), (40, 535))



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
                print(f"Invalid vehicle at line {i} → {line}: {e}")
                raise
    return Problem(vehicles)

def solve():
    global solution, current_step, no_solution_found, playing
    playing = False # Prevent auto-play when solving a new map
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
    no_solution_found = (len(solution) == 0)

# Main loop
running = True
screen_state = "home"
problem = load_map(maps[map_idx])

if __name__ == "__main__":
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
                        click_sound.play()
                        screen_state = "play"
                        problem = load_map(maps[map_idx])
                        solution = []
                        current_step = 0
                        playing = False
                    elif 310 <= x <= 490 and 370 <= y <= 420:
                        click_sound.play()
                        running = False
                elif screen_state == "play":
                    # Map/Solver arrows
                    if 90 <= x <= 110:
                        if 70 <= y <= 95:  # Map <
                            click_sound.play()
                            map_idx = (map_idx - 1) % len(maps)
                            problem = load_map(maps[map_idx])
                            solution = []
                            current_step = 0
                        elif 100 <= y <= 125:  # Solver <
                            click_sound.play()
                            solver_idx = (solver_idx - 1) % len(solvers)
                    elif 193 <= x <= 213:
                        if 70 <= y <= 95:  # Map >
                            click_sound.play()
                            map_idx = (map_idx + 1) % len(maps)
                            problem = load_map(maps[map_idx])
                            solution = []
                            current_step = 0
                        elif 100 <= y <= 125:  # Solver >
                            click_sound.play()
                            solver_idx = (solver_idx + 1) % len(solvers)

                    # Buttons: Solve / Play / Reset / Return
                    if 50 <= x <= 170:
                        if 170 <= y <= 210:  # Solve
                            click_sound.play()
                            solve()
                        elif 230 <= y <= 270:  # Play
                            click_sound.play()
                            playing = not playing
                        elif 290 <= y <= 330:  # Reset
                            click_sound.play()
                            current_step = 0
                            playing = False
                        elif 350 <= y <= 390:  # Return to home
                            click_sound.play()
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
