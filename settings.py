from tkinter import Button, Image, ttk
import tkinter as tk
from PIL import Image, ImageTk
class Settings():
    def __init__(self, master, gui):
        self.master = master
        self.gui = gui
        self.gui_outline()
    def gui_outline(self):
        self.duty_frame = ttk.Frame(self.master)
        self.duty_menu()
        self.duty_frame.pack(fill="x")
    def duty_menu(self):
        self.duty_label = ttk.Label(self.duty_frame, text="Pump Duty Cycle Set")
        self.duty_label.pack()

        self.image = Image.open("filter.png").resize((64, 64))
        self.filter_image = ImageTk.PhotoImage(self.image)
        self.filter_image_label = Button(
            self.duty_frame, command=self.gui.toggle_pump, image = self.filter_image, borderwidth= 0, highlightthickness=0, background= "#18191A", foreground= "#18191A")
        #     ##Above fix the image, apparently its about the borderwidth and height thickness or something. figure out the method
        #     #for a ttk button
        self.filter_image_label.pack()

        time_start_label = ttk.Label(self.duty_frame, text="Minutes in Hour to Start Pump (0 - 59 minutes)")
        time_start_label.pack()

        self.time_start = tk.IntVar(value=0)
        vcmd_start = (self.duty_frame.register(self.check_time_start), "%P")
        self.time_start_entry = ttk.Entry(self.duty_frame, textvariable=self.time_start, validate="focusout", validatecommand=vcmd_start)
        self.time_start_entry.pack()

        time_duration_label = ttk.Label(self.duty_frame, text = "Duration that Pump is On (0-10 minutes)")
        time_duration_label.pack()

        self.time_duration = tk.IntVar(value=0)
        vcmd_duration = (self.duty_frame.register(self.check_time_duration), "%P")
        self.time_duration_entry = ttk.Entry(self.duty_frame, textvariable=self.time_duration, validate="focusout", validatecommand=vcmd_duration)
        self.time_duration_entry.pack()

        self.apply_button = ttk.Button(self.duty_frame, text="Apply", command=self.apply_settings)
        self.apply_button.pack()

    def apply_settings(self):
        print("Applying Settings")
        self.apply_button.config(state="disabled")
        self.gui.apply_settings(self.time_start.get(), self.time_duration.get())
    def check_time_start(self, value):
        if not value.isdigit():
            self.time_start.set(0)
        else:
            if int(value) > 59:
                self.time_start.set(59)
            if int(value) < 0:
                self.time_start.set(0)
        self.apply_button.config(state="normal")
        return False
    def check_time_duration(self, value):
        if not value.isdigit():
            self.time_duration.set(0)
        else:
            if int(value) > 10:
                self.time_duration.set(10)
            if int(value) < 0:
                self.time_duration.set(0)
        return False