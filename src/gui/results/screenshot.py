import tkinter as tk


class ScreenshotFrameContainer:
    def __init__(self, parent):
        self.parent = parent

        self.frame = tk.Frame(
            self.parent.frame, bd=1, relief=tk.SOLID)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
