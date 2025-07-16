import tkinter as tk
import math
import time
import threading

# Window and diagram size constants
WIDTH = 600
HEIGHT = 600
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
RADIUS = 200

# Visual styling for special numbers and elements
TESLA_NUMBERS = [3, 6, 9]
TESLA_COLOR = "cyan"
DEFAULT_COLOR = "white"
LINE_COLOR = "yellow"
GLOW_COLOR = "blue"

# Doubling sequence (ignores Tesla numbers)
DOUBLING_SEQUENCE = [1, 2, 4, 8, 7, 5, 1]

# Create the main application window
root = tk.Tk()
root.title("Tesla 3-6-9 Animated Diagram")
root.configure(bg="black")

# Add a canvas to draw the diagram
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
canvas.pack()

# Converts angle and radius to (x, y) canvas coordinates
def get_coordinates(angle_deg, radius):
    angle_rad = math.radians(angle_deg)
    x = CENTER_X + radius * math.cos(angle_rad)
    y = CENTER_Y + radius * math.sin(angle_rad)
    return x, y

# Draws the numbers 1–9 in a circular layout and highlights 3,6,9
def draw_circle():
    for i in range(1, 10):
        angle = (i - 1) * 40  # 360/9 = 40 degrees apart
        x, y = get_coordinates(angle - 90, RADIUS)
        color = TESLA_COLOR if i in TESLA_NUMBERS else DEFAULT_COLOR

        # Optional glowing background for Tesla numbers
        if i in TESLA_NUMBERS:
            canvas.create_oval(x - 24, y - 24, x + 24, y + 24, fill=GLOW_COLOR, outline="", width=0)

        # Main circle for each number
        canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="black", outline=color, width=2)
        canvas.create_text(x, y, text=str(i), fill=color, font=("Helvetica", 16, "bold"))

# Static lines connecting doubling sequence
def draw_static_lines():
    coords = []
    for num in DOUBLING_SEQUENCE:
        angle = (num - 1) * 40
        x, y = get_coordinates(angle - 90, RADIUS)
        coords.append((x, y))
    for i in range(len(coords) - 1):
        canvas.create_line(coords[i][0], coords[i][1], coords[i + 1][0], coords[i + 1][1], fill=LINE_COLOR, width=2, arrow=tk.LAST)

# Rotating spiral visual energy vortex
def draw_spiral():
    num_loops = 4
    points = []
    for t in range(0, 360 * num_loops, 5):
        angle = math.radians(t)
        r = (t / (360 * num_loops)) * RADIUS
        x = CENTER_X + r * math.cos(angle)
        y = CENTER_Y + r * math.sin(angle)
        points.append((x, y))
    for i in range(len(points) - 1):
        canvas.create_line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], fill="gray20")

# Animation for energy flow line between numbers
def animate_lines():
    coords = []
    for num in DOUBLING_SEQUENCE:
        angle = (num - 1) * 40
        x, y = get_coordinates(angle - 90, RADIUS)
        coords.append((x, y))
    while True:
        for i in range(len(coords) - 1):
            line = canvas.create_line(
                coords[i][0], coords[i][1],
                coords[i + 1][0], coords[i + 1][1],
                fill=LINE_COLOR, width=3, arrow=tk.LAST
            )
            root.update()
            time.sleep(0.5)
            canvas.delete(line)

# Starts animation in a separate thread so GUI doesn't freeze
def start_animation():
    threading.Thread(target=animate_lines, daemon=True).start()

# Run all draw functions
draw_spiral()
draw_circle()
draw_static_lines()
start_animation()

# Start GUI loop
root.mainloop()
