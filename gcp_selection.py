#gcp_selection.py

"""This file will contain the code that opens a GUI based GCP selection tool."""

#import neccesary packages and modules
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

class ImageViewer(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<MouseWheel>", self.on_zoom)

        self.image = None
        self.tk_img = None
        self.scale = 1.0
        self.canvas_origin = (0, 0)
        self.img_pos = (0, 0)  # Top-left corner of the image on the canvas

    def create_widgets(self):
        self.canvas = tk.Canvas(self, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def open_image(self):
        filepath = filedialog.askopenfilename()
        if not filepath:
            return

        self.image = Image.open(filepath)
        self.img_pos = (0, 0)
        self.fit_image_to_window()
        self.update_image()

    def fit_image_to_window(self):
        if self.image:
            img_width, img_height = self.image.size
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            scale_x = canvas_width / img_width
            scale_y = canvas_height / img_height
            self.scale = min(scale_x, scale_y)

    def update_image(self):
        if self.image:
            width, height = self.image.size
            scaled_width, scaled_height = int(width * self.scale), int(height * self.scale)
            img = self.image.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
            self.tk_img = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(self.img_pos[0], self.img_pos[1], anchor=tk.NW, image=self.tk_img)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_click(self, event):
        self.canvas_origin = (event.x, event.y)

    def on_drag(self, event):
        dx = event.x - self.canvas_origin[0]
        dy = event.y - self.canvas_origin[1]
        self.canvas.move(tk.ALL, dx, dy)
        self.img_pos = (self.img_pos[0] + dx, self.img_pos[1] + dy)
        self.canvas_origin = (event.x, event.y)

    def on_zoom(self, event):
        scale_factor = 1.1 if event.delta > 0 else 0.9
        mouse_x = self.canvas.canvasx(event.x)
        mouse_y = self.canvas.canvasy(event.y)
        offset_x = (mouse_x - self.img_pos[0]) * (scale_factor - 1)
        offset_y = (mouse_y - self.img_pos[1]) * (scale_factor - 1)
        self.scale *= scale_factor
        self.img_pos = (self.img_pos[0] - offset_x, self.img_pos[1] - offset_y)
        self.update_image()

    def submit_action(self):
        print("Selected Option:", self.radio_var.get())
        print("Entry 1:", self.entry1.get())
        print("Entry 2:", self.entry2.get())

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Viewer")
        self.geometry("1200x800")  # Set initial window size
        self.minsize(600, 400)  # Set minimum window size

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky="nsew")

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Image Frame
        image_frame = ttk.Frame(main_frame)
        image_frame.grid(row=0, column=0, sticky="nsew")
        self.image_viewer = ImageViewer(master=image_frame)

        # Control Panel
        control_panel = ttk.Frame(self)
        control_panel.grid(row=0, column=1, sticky="ns")

        open_btn = ttk.Button(control_panel, text="Open Image", command=self.image_viewer.open_image)
        open_btn.pack(pady=5)

        self.radio_var = tk.StringVar()
        self.radio_var.set("Option 1")

        tk.Radiobutton(control_panel, text="Option 1", variable=self.radio_var, value="Option 1").pack(anchor=tk.W)
        tk.Radiobutton(control_panel, text="Option 2", variable=self.radio_var, value="Option 2").pack(anchor=tk.W)

        self.entry1 = ttk.Entry(control_panel)
        self.entry1.pack(pady=5)
        self.entry2 = ttk.Entry(control_panel)
        self.entry2.pack(pady=5)

        submit_btn = ttk.Button(control_panel, text="Submit", command=self.submit_action)
        submit_btn.pack(pady=5)

    def submit_action(self):
        print("Selected Option:", self.radio_var.get())
        print("Entry 1:", self.entry1.get())
        print("Entry 2:", self.entry2.get())

if __name__ == "__main__":
    app = App()
    app.update_idletasks()
    app.image_viewer.fit_image_to_window()
    app.mainloop()
