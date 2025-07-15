# Import the tkinter module for GUI
import tkinter as tk

# Import math module for logarithmic calculations
import math

# ------------------------------------------
# CONSTANT DATA DEFINITIONS
# ------------------------------------------

# Define the major bands of the electromagnetic spectrum with wavelength ranges and color representation
EM_BANDS = [
    {"name": "Radio",        "min_wl": 1e0,     "max_wl": 1e3,    "color": "gray"},
    {"name": "Microwave",    "min_wl": 1e-3,    "max_wl": 1e0,    "color": "purple"},
    {"name": "Infrared",     "min_wl": 7e-7,    "max_wl": 1e-3,   "color": "darkred"},
    {"name": "Visible",      "min_wl": 4e-7,    "max_wl": 7e-7,   "color": "white"},
    {"name": "Ultraviolet",  "min_wl": 1e-8,    "max_wl": 4e-7,   "color": "blue"},
    {"name": "X-Rays",       "min_wl": 1e-11,   "max_wl": 1e-8,   "color": "skyblue"},
    {"name": "Gamma Rays",   "min_wl": 1e-14,   "max_wl": 1e-11,  "color": "cyan"},
]

# Sun's emission strength for each EM band (used for bar height and label)
SUN_EMISSION_STRENGTH = {
    "Radio":      ("Low", 25),
    "Microwave":  ("Low", 25),
    "Infrared":   ("High", 80),
    "Visible":    ("Very High", 120),
    "Ultraviolet":("Moderate", 50),
    "X-Rays":     ("Low", 25),
    "Gamma Rays": ("Very Low", 10),
}

# Common synthetic light sources and which EM bands they emit within
LIGHT_SOURCES = [
    {"name": "Incandescent", "regions": ["Visible", "Infrared"], "color": "orange"},
    {"name": "Halogen",      "regions": ["Visible", "Infrared"], "color": "gold"},
    {"name": "Fluorescent",  "regions": ["Ultraviolet", "Visible"], "color": "lime"},
    {"name": "LED",          "regions": ["Visible"], "color": "yellow"},
    {"name": "Laser",        "regions": ["Visible"], "color": "red"},
    {"name": "Microwave",    "regions": ["Microwave"], "color": "violet"},
    {"name": "UV Lamp",      "regions": ["Ultraviolet"], "color": "deepskyblue"},
]

# ------------------------------------------
# FUNCTION: Convert wavelength to X position on canvas
# ------------------------------------------
def wavelength_to_x(wavelength, width):
    min_log = math.log10(1e-14)     # log-scale min (smallest wavelength)
    max_log = math.log10(1e3)       # log-scale max (largest wavelength)
    wl_log = math.log10(wavelength) # convert wavelength to log scale
    # Normalize log value to canvas width
    return int((wl_log - min_log) / (max_log - min_log) * width)

# ------------------------------------------
# FUNCTION: Retrieve EM band dictionary by name
# ------------------------------------------
def get_band_by_name(name):
    for band in EM_BANDS:
        if name.lower() in band["name"].lower():
            return band
    return None

# ------------------------------------------
# GUI SETUP
# ------------------------------------------

# Create the root application window
root = tk.Tk()
root.title("🌞 Synthetic Lights + Sun Emission on EM Spectrum")  # Window title

# Create a resizable canvas widget
canvas = tk.Canvas(root, width=1200, height=700, bg="black")  # black background
canvas.pack(fill="both", expand=True)  # Fill window and expand when resized

# ------------------------------------------
# MAIN DRAW FUNCTION
# ------------------------------------------
def draw():
    canvas.delete("all")  # Clear all drawings on canvas
    width = canvas.winfo_width()     # Get current canvas width
    height = canvas.winfo_height()   # Get current canvas height

    # Layout positions for drawing elements
    spectrum_mid = int(height * 0.3)       # Middle of EM spectrum bar
    sun_base = spectrum_mid - 60           # Y-position for sun emission bars
    synthetic_base = int(height * 0.55)    # Y-position to start synthetic lights
    bar_height = 25                        # Height of synthetic light bars
    gap = 5                                # Gap between synthetic light bars

    # ----- Draw EM spectrum bands -----
    for band in EM_BANDS:
        # Convert min and max wavelengths to canvas X-coordinates
        x1 = wavelength_to_x(band["max_wl"], width)
        x2 = wavelength_to_x(band["min_wl"], width)

        # Draw rectangle for EM band
        canvas.create_rectangle(x1, spectrum_mid - 40, x2, spectrum_mid + 40,
                                fill=band["color"], outline="white")

        # Draw band label at the center
        canvas.create_text((x1 + x2)//2, spectrum_mid,
                           text=band["name"], fill="black" if band["color"] != "white" else "black",
                           font=("Helvetica", 12, "bold"))

        # ----- Draw sun emission bar -----
        strength_label, strength_height = SUN_EMISSION_STRENGTH.get(band["name"], ("None", 0))
        cx = (x1 + x2)//2  # center X position of the band
        # Draw vertical sun emission bar
        canvas.create_rectangle(cx - 10, sun_base - strength_height, cx + 10, sun_base,
                                fill="orange", outline="gold")
        # Label the strength of sun emission
        canvas.create_text(cx, sun_base - strength_height - 10,
                           text=strength_label, fill="white", font=("Arial", 9, "italic"))

    # ----- Draw synthetic light source emission bars -----
    for i, source in enumerate(LIGHT_SOURCES):
        y = synthetic_base + i * (bar_height + gap)  # Y position for each light source

        # For each region the light source emits in
        for region_name in source["regions"]:
            band = get_band_by_name(region_name)
            if band:
                # Convert region's wavelength range to X-coordinates
                x1 = wavelength_to_x(band["max_wl"], width)
                x2 = wavelength_to_x(band["min_wl"], width)

                # Draw the light bar
                canvas.create_rectangle(x1, y, x2, y + bar_height,
                                        fill=source["color"], outline="white")

        # Label the name of the light source
        canvas.create_text(10, y + bar_height // 2, anchor="w",
                           text=source["name"], fill="white", font=("Arial", 11, "bold"))

    # ----- Draw wavelength scale (logarithmic) -----
    for exp in range(-14, 4):  # From 1e-14 m to 1e3 m
        wl = 10**exp
        x = wavelength_to_x(wl, width)

        # Draw tick mark
        canvas.create_line(x, spectrum_mid + 45, x, spectrum_mid + 55, fill="white")

        # Label tick
        canvas.create_text(x, spectrum_mid + 70, text=f"1e{exp} m",
                           fill="white", font=("Arial", 9))

    # Label for wavelength axis
    canvas.create_text(width // 2, spectrum_mid + 95, text="Wavelength (log scale, meters)",
                       fill="white", font=("Arial", 11, "italic"))

# Redraw everything when the window is resized
root.bind("<Configure>", lambda e: draw())

# Initial drawing
draw()

# Start the GUI event loop
root.mainloop()
