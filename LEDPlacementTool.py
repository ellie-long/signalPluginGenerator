import tkinter as tk
from tkinter import filedialog, messagebox
import json
from PIL import Image, ImageTk
import numpy as np
from scipy.interpolate import splprep, splev

class LEDStripEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("SignalRGB Plugin Creator")

        self.num_leds = 10  # Default number of LEDs
        self.led_positions = []
        self.spline_points = []
        self.background_image = None
        self.bg_image_id = None
        self.drawing_spline = False

        self.canvas = tk.Canvas(root, width=400, height=400, bg="black")
        self.canvas.pack()

        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack()

        self.num_leds_label = tk.Label(self.controls_frame, text="Number of LEDs:")
        self.num_leds_label.grid(row=0, column=0)
        
        self.num_leds_entry = tk.Entry(self.controls_frame)
        self.num_leds_entry.grid(row=0, column=1)
        self.num_leds_entry.insert(0, str(self.num_leds))

        self.spline_button = tk.Button(self.controls_frame, text="Draw Spline", command=self.toggle_spline_mode)
        self.spline_button.grid(row=0, column=2)

        self.place_leds_button = tk.Button(self.controls_frame, text="Place LEDs on Spline", command=self.place_leds_on_spline)
        self.place_leds_button.grid(row=0, column=3)

        self.upload_button = tk.Button(self.controls_frame, text="Upload Background", command=self.upload_background)
        self.upload_button.grid(row=0, column=4)

        self.output_button = tk.Button(self.controls_frame, text="Output Plugin", command=self.output_plugin)
        self.output_button.grid(row=0, column=5)

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.draw_leds()

    def draw_leds(self):
        self.canvas.delete("all")
        if self.background_image:
            self.bg_image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)
        for x, y in self.spline_points:
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue")
        for i, pos in enumerate(self.led_positions):
            x, y = pos
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red", outline="white")
            self.canvas.create_text(x, y - 15, text=str(i), fill="white")

    def toggle_spline_mode(self):
        self.drawing_spline = not self.drawing_spline
        if self.drawing_spline:
            self.spline_button.config(relief=tk.SUNKEN)
        else:
            self.spline_button.config(relief=tk.RAISED)

    def on_canvas_click(self, event):
        if self.drawing_spline:
            self.spline_points.append((event.x, event.y))
            self.draw_leds()

    def place_leds_on_spline(self):
        try:
            num_leds = int(self.num_leds_entry.get())
            if num_leds < 1:
                raise ValueError("Number of LEDs must be at least 1.")
            self.num_leds = num_leds
            if len(self.spline_points) < 2:
                raise ValueError("At least two points are needed to create a spline.")
            
            points = np.array(self.spline_points)
            tck, _ = splprep([points[:, 0], points[:, 1]], s=0)
            u = np.linspace(0, 1, num_leds)
            spline = splev(u, tck)
            self.led_positions = list(zip(spline[0], spline[1]))
            self.draw_leds()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def upload_background(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            img = Image.open(file_path)
            img = img.resize((800, 800), Image.LANCZOS)
            self.background_image = ImageTk.PhotoImage(img)
            self.draw_leds()

    def output_plugin(self):
        # Determine initial width and height based on max coordinates
        max_x = max(int(x) for x, y in self.led_positions) + 1
        max_y = max(int(y) for x, y in self.led_positions) + 1

        # Scale coordinates to fit within num_leds x num_leds
        scale_factor_x = self.num_leds / max_x
        scale_factor_y = self.num_leds / max_y

        scaled_positions = [
            [int(x * scale_factor_x), int(y * scale_factor_y)]
            for x, y in self.led_positions
        ]

        # Recalculate width and height after scaling
        final_width = max(x for x, y in scaled_positions) + 1
        final_height = max(y for x, y in scaled_positions) + 1

        led_mapping = list(range(self.num_leds))
        led_names = [f"Led{i + 1}" for i in range(self.num_leds)]

        plugin_data = {
            "ProductName": "Custom LED Strip",
            "DisplayName": f"Custom LED Strip - {self.num_leds} LED",
            "Brand": "CompGen",
            "Type": "custom",
            "LedCount": self.num_leds,
            "Width": final_width,
            "Height": final_height,
            "LedMapping": led_mapping,
            "LedCoordinates": scaled_positions,
            "LedNames": led_names
        }

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as f:
                json.dump(plugin_data, f, indent=4)
            messagebox.showinfo("Success", "Plugin saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = LEDStripEditor(root)
    root.mainloop()
