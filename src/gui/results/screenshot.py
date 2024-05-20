import tkinter as tk
from PIL import ImageTk, Image


class ScreenshotFrameContainer:
    def __init__(self, parent):
        self.parent = parent

        self.frame = tk.Frame(
            self.parent.frame, bd=1, relief=tk.SOLID)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH)

        self.screenshot_src = ""

    def set_screenshot(self, src):
        self.screenshot_src = src
        self.screenshot = ImageTk.PhotoImage(Image.open(src))

        self.__create_image_frame()

    def __create_image_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        panel = tk.Canvas(self.frame, bd=0, highlightthickness=0)
        panel.create_image(0, 0, image=self.screenshot,
                           anchor=tk.NW, tags="IMG")
        panel.grid(row=0, sticky=tk.NSEW)
        panel.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
