# =======================
# Chakra Frequency Visualizer Dependencies
# =======================
#
# Python packages (install via pip):
#   numpy
#   pygame
#   matplotlib
#
# Install via:
#   pip install numpy pygame matplotlib
#
# ------------------------------------------------
# Debian/Ubuntu system packages (install via apt):
#   build-essential        # compiler and build tools (if compiling extensions)
#   python3-dev            # Python headers for compiling packages
#   libglib2.0-0           # GTK threading library needed by pygame audio
#   libsdl2-mixer-2.0-0    # SDL2 audio mixer library for pygame sound
#   libfreetype6-dev       # For matplotlib font rendering
#   libpng-dev             # For matplotlib image support
#   libjpeg-dev            # For matplotlib image support
#
# Install system packages with:
#   sudo apt update
#   sudo apt install build-essential python3-dev libglib2.0-0 libsdl2-mixer-2.0-0 libfreetype6-dev libpng-dev libjpeg-dev
#
# ------------------------------------------------
# Notes:
# - tkinter usually comes preinstalled; if missing, install:
#     sudo apt install python3-tk
# - pygame requires SDL2 and related libs to play sound correctly
# - matplotlib requires image libs for full feature set
# 
# =======================
import tkinter as tk
from tkinter import ttk
import threading
import numpy as np
import pygame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize pygame mixer for audio playback
pygame.mixer.init(frequency=44100, size=-16, channels=1)

# Chakra data
chakras = [
    {"name": "Root", "frequency": 396, "color": "#ff0000", "description": "Grounding, survival, stability.", "affirmation": "I am safe and secure."},
    {"name": "Sacral", "frequency": 417, "color": "#ff7f00", "description": "Creativity, pleasure, emotions.", "affirmation": "I am creative and joyful."},
    {"name": "Solar Plexus", "frequency": 528, "color": "#ffff00", "description": "Confidence, power, self-esteem.", "affirmation": "I am strong and confident."},
    {"name": "Heart", "frequency": 639, "color": "#00ff00", "description": "Love, compassion, healing.", "affirmation": "I am open to love."},
    {"name": "Throat", "frequency": 741, "color": "#0000ff", "description": "Communication, truth, expression.", "affirmation": "I express myself freely."},
    {"name": "Third Eye", "frequency": 852, "color": "#4b0082", "description": "Intuition, insight, vision.", "affirmation": "I trust my intuition."},
    {"name": "Crown", "frequency": 963, "color": "#8f00ff", "description": "Spirituality, connection, enlightenment.", "affirmation": "I am connected to the divine."}
]

# Generate and play tone with pygame
def play_sound(freq):
    def generate_and_play():
        duration = 0.5  # seconds
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        tone = np.sin(2 * np.pi * freq * t)
        audio = (tone * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(audio)
        sound.play()
    threading.Thread(target=generate_and_play, daemon=True).start()

# Tkinter UI setup
root = tk.Tk()
root.title("🧘 Chakra Frequency Visualizer (with scrollbar)")
root.geometry("700x800")
root.configure(bg="black")

# Main frame with scrollbar
main_frame = tk.Frame(root, bg="black")
main_frame.pack(fill=tk.BOTH, expand=True)

# Canvas for scrollable content
canvas = tk.Canvas(main_frame, bg="black", highlightthickness=0)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar widget
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)

# Frame inside canvas to hold chakra widgets
scrollable_frame = tk.Frame(canvas, bg="black")

# Update scrollregion when content changes size
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", on_frame_configure)

# Add scrollable_frame to canvas window
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Header label
tk.Label(scrollable_frame, text="🌈 Chakras & Frequencies",
         font=("Helvetica", 24, "bold"), fg="white", bg="black").pack(pady=20)

# Frequency bar chart plot
def plot_frequencies():
    freqs = [chakra['frequency'] for chakra in chakras]
    names = [chakra['name'] for chakra in chakras]
    fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
    ax.bar(names, freqs, color=[chakra["color"] for chakra in chakras])
    ax.set_title("Chakra Frequencies (Hz)")
    ax.set_ylabel("Frequency (Hz)")
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.tick_params(colors='white')
    ax.title.set_color('white')
    ax.yaxis.label.set_color('white')
    for spine in ax.spines.values():
        spine.set_color('white')
    canvas_plot = FigureCanvasTkAgg(fig, master=scrollable_frame)
    canvas_plot.draw()
    canvas_plot.get_tk_widget().pack(pady=20)

# Create chakra widgets
for chakra in chakras:
    frame = tk.Frame(scrollable_frame, bg="black")
    frame.pack(pady=10, fill=tk.X, padx=40)

    color_circle = tk.Canvas(frame, width=60, height=60, bg="black", highlightthickness=0)
    color_circle.create_oval(5, 5, 55, 55, fill=chakra["color"], outline="")
    color_circle.pack(side=tk.LEFT)

    info_frame = tk.Frame(frame, bg="black")
    info_frame.pack(side=tk.LEFT, padx=20)

    tk.Label(info_frame, text=f"{chakra['name']} Chakra", font=("Helvetica", 16, "bold"),
             fg=chakra["color"], bg="black").pack(anchor="w")
    tk.Label(info_frame, text=f"Frequency: {chakra['frequency']} Hz", font=("Helvetica", 12),
             fg="white", bg="black").pack(anchor="w")
    tk.Label(info_frame, text=f"Color Code: {chakra['color']}", font=("Helvetica", 12),
             fg="white", bg="black").pack(anchor="w")
    tk.Label(info_frame, text=f"🌀 {chakra['description']}", font=("Helvetica", 10),
             fg="gray", bg="black").pack(anchor="w")
    tk.Label(info_frame, text=f"💬 Affirmation: {chakra['affirmation']}", font=("Helvetica", 10, "italic"),
             fg="lightgray", bg="black").pack(anchor="w")

    tk.Button(info_frame, text="🔊 Play Frequency",
              command=lambda f=chakra['frequency']: play_sound(f),
              bg="gray20", fg="white", relief=tk.RIDGE).pack(anchor="w", pady=4)

# Add the frequency bar chart
plot_frequencies()

# Run the Tkinter event loop
root.mainloop()
