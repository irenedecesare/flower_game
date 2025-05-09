import random
import tkinter as tk
from tkinter import messagebox
from collections import deque

GRID_SIZE = 7
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
ALL_DIRS = DIRS + [(-1, -1), (-1, 1), (1, -1), (1, 1)]

def in_bounds(r, c):
    return 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE

def create_empty_grid():
    return [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def generate_flower_solution(row_vect):
    def is_valid(r, c, flowers):
        for fr, fc in flowers:
            if fc == c or abs(fr - r) <= 1 and abs(fc - c) <= 1:
                return False
        return True

    def place_flowers(rows_left, flowers):
        if not rows_left:
            return flowers
        row = rows_left[0]
        remaining = rows_left[1:]
        cols = list(range(GRID_SIZE))
        random.shuffle(cols)
        for col in cols:
            if is_valid(row, col, flowers):
                result = place_flowers(remaining, flowers + [(row, col)])
                if result:
                    return result
        return None

    return place_flowers(row_vect, [])

def create_connected_regions(flowers):
    occupied = set()
    region_map = [[-1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    area_dict = {}

    aree_regioni = random.choices([1, 2, 3, 4, 5, 6, 7, 8], weights=[3, 5, 5, 4, 3, 3, 2, 2], k=GRID_SIZE)
    #print(aree_regioni)

    random.shuffle(flowers)
    for idx, (r, c) in enumerate(flowers):
        target_area = aree_regioni[idx]
        region = set()
        queue = deque([(r, c)])
        region.add((r, c))
        occupied.add((r, c))
        rndm_DIRS = []

        while len(region) < target_area and queue:
            cr, cc = queue.popleft()
            for elem in DIRS:
                random.shuffle(DIRS)
                rndm_DIRS.append(DIRS[0])

            for dr, dc in rndm_DIRS:
                nr, nc = cr + dr, cc + dc
                if in_bounds(nr, nc) and (nr, nc) not in occupied:
                    region.add((nr, nc))
                    occupied.add((nr, nc))
                    queue.append((nr, nc))
                    if len(region) == target_area:
                        break

        for (rr, cc) in region:
            region_map[rr][cc] = idx
        area_dict[idx] = list(region)
    
    # collect all adiacent unassigned cells
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if region_map[r][c] == -1:
                queue = deque([(r, c)])
                to_fill = [(r, c)]
                region_map[r][c] = -2
                while queue:
                    cr, cc = queue.popleft()
                    for dr, dc in DIRS:
                        nr, nc = cr + dr, cc + dc
                        if in_bounds(nr, nc) and region_map[nr][nc] == -1:
                            region_map[nr][nc] = -2
                            queue.append((nr, nc))
                            to_fill.append((nr, nc))

                # Find a region to add the unassigned cells
                found_region = None
                for tr, tc in to_fill:
                    for dr, dc in DIRS:
                        nr, nc = tr + dr, tc + dc
                        if in_bounds(nr, nc) and region_map[nr][nc] >= 0:
                            found_region = region_map[nr][nc]
                            break
                    if found_region is not None:
                        break

                if found_region is not None:
                    for tr, tc in to_fill:
                        region_map[tr][tc] = found_region
                        area_dict[found_region].append((tr, tc))
                else:
                    raise RuntimeError("Error during the assignment of cells to region.")

    return region_map, area_dict

def generate_game_setup():
    max_attempts = 1000
    for _ in range(max_attempts):
        row_vect = list(range(GRID_SIZE))
        random.shuffle(row_vect)
        flowers = generate_flower_solution(row_vect)
        if len(flowers)<GRID_SIZE:
            continue
        region_map, area_dict = create_connected_regions(flowers)
        if region_map:
            grid = create_empty_grid()
            region_colors = generate_region_colors(len(area_dict))
            return grid, region_map, area_dict, flowers, region_colors
    raise RuntimeError("Setup unavailable.")

def generate_region_colors(region_count):
    fixed_palettes = {
        #6: ["#FFB6C1", "#ADD8E6", "#90EE90", "#FFD700", "#FFA07A", "#DDA0DD"],
        7: ["#FFB6C1", "#ADD8E6", "#90EE90", "#FFD700", "#FFA07A", "#DDA0DD", "#A9A9A9"]#,
        #8: ["#FFB6C1", "#ADD8E6", "#90EE90", "#FFD700", "#FFA07A", "#DDA0DD", "#A9A9A9", "#00CED1"]
    }

    if region_count not in fixed_palettes:
        raise ValueError(f"Check that REGION COUNT --> {region_count} must be the same as the colors in the palette.")

    colors = fixed_palettes[region_count]
    return {idx: colors[idx] for idx in range(region_count)}


def redraw_canvas(canvas, grid, region_map, area_dict, region_colors, cell_size=60):
    canvas.delete("all")
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            region_id = region_map[r][c]
            if region_id != -1:
                color = region_colors[region_id]
                canvas.create_rectangle(
                    c * cell_size, r * cell_size,
                    (c + 1) * cell_size, (r + 1) * cell_size,
                    fill=color, outline="black"
                )
            symbol = grid[r][c]
            if symbol:
                canvas.create_text(
                    c * cell_size + cell_size / 2,
                    r * cell_size + cell_size / 2,
                    text=symbol, font=("Arial", 20)
                )

def handle_click(event, canvas, grid, region_map, area_dict, region_colors, cell_size=60):
    col = event.x // cell_size
    row = event.y // cell_size
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        current = grid[row][col]
        if current == "":
            grid[row][col] = "❌"
        elif current == "❌":
            grid[row][col] = "🌸"
        elif current == "🌸":
            grid[row][col] = ""
        redraw_canvas(canvas, grid, region_map, area_dict, region_colors)

def clear_grid(grid, canvas, region_map, area_dict, region_colors):
    global hints_used
    hints_used["count"] = 0
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            grid[r][c] = ""
    redraw_canvas(canvas, grid, region_map, area_dict, region_colors)

def check_solution(grid, region_map):
    rows = [0]*GRID_SIZE
    cols = [0]*GRID_SIZE
    regions = {}

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == "🌸":
                rows[r] += 1
                cols[c] += 1
                region_id = region_map[r][c]
                regions[region_id] = regions.get(region_id, 0) + 1
                for dr, dc in ALL_DIRS:
                    nr, nc = r + dr, c + dc
                    if in_bounds(nr, nc) and (dr != 0 and dc != 0):
                        if grid[nr][nc] == "🌸":
                            return False

    if any(count != 1 for count in rows + cols):
        return False
    if any(count != 1 for count in regions.values()):
        return False

    return True

def new_puzzle():
    global grid, region_map, area_dict, region_colors, flowers, hints_used
    grid, region_map, area_dict, flowers, region_colors = generate_game_setup()
    hints_used = {"count": 0}
    redraw_canvas(canvas, grid, region_map, area_dict, region_colors)

def use_hint(grid, flowers, hints_used, canvas, region_map, area_dict):
    if hints_used["count"] < len(flowers):
        r, c = flowers[hints_used["count"]]
        grid[r][c] = "🌸"
        hints_used["count"] += 1
        redraw_canvas(canvas, grid, region_map, area_dict, region_colors)

# Globals
canvas = None
grid = None
region_map = None
area_dict = None
region_colors = None
flowers = None
hints_used = None


def start_game():
    global canvas, grid, region_map, area_dict, region_colors, flowers, hints_used

    hints_used = {"count": 0}

    grid, region_map, area_dict, flowers, region_colors = generate_game_setup()
    print(grid)
    print(region_map)

    window = tk.Tk()
    window.title("Flower Puzzle")

    canvas = tk.Canvas(window, width=GRID_SIZE * 60, height=GRID_SIZE * 60)
    canvas.pack()

    redraw_canvas(canvas, grid, region_map, area_dict, region_colors)

    canvas.bind("<Button-1>", lambda event: handle_click(event, canvas, grid, region_map, area_dict, region_colors))

    # Buttons
    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    # Style
    button_style = {
        "font": ("Arial", 12),
        "width": 10,
        "height": 1,
        "bg": "#f0f0f0",
        "relief": "raised",
        "bd": 2
    }

    check_button = tk.Button(button_frame, text="Check", **button_style, command=lambda: (
        messagebox.showinfo("Result", "✔️ Correct!" if check_solution(grid, region_map) else "❌ Error!")))
    clear_button = tk.Button(button_frame, text="Clear", **button_style, command=lambda: clear_grid(grid, canvas, region_map, area_dict, region_colors))
    new_button = tk.Button(button_frame, text="New Puzzle", **button_style, command=new_puzzle)
    hint_button = tk.Button(button_frame, text="Hint", **button_style,
                            command=lambda: use_hint(grid, flowers, hints_used, canvas, region_map, area_dict))
    hint_button.pack(side="left", padx=5)


    check_button.pack(side="left", padx=5)
    clear_button.pack(side="left", padx=5)
    new_button.pack(side="left", padx=5)

    window.mainloop()

start_game()
