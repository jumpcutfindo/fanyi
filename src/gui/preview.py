import tkinter as tk
from PIL import ImageTk, Image
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui import MainFrameContainer

from gui.utils import get_scaled_size

class PreviewFrameContainer:
    def __init__(self, root: "MainFrameContainer", title: str, screenshot_file: str):
        self.root = root
        self.window = tk.Toplevel()
        self.window.geometry(f'{self.root.scaled(800)}x{self.root.scaled(600)}')
        self.window.title(title)

        self.frame = tk.Frame(self.window)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.screenshot = Image.open(screenshot_file)

        self.photo_image = ImageTk.PhotoImage(self.screenshot)
        self.image_label = tk.Label(self.frame, image=self.photo_image)
        self.image_label.grid(row=0, column=0, sticky=tk.NSEW)

        self.frame.bind('<Configure>', self.__on_resize)

    def show(self):
        self.window.mainloop()

    def __on_resize(self, event):
        width, height = get_scaled_size(
            self.frame.winfo_width(), self.frame.winfo_height(), self.screenshot.width, self.screenshot.height)

        self.photo_image = ImageTk.PhotoImage(
            self.screenshot.resize(size=(width, height)))

        self.image_label.configure(image=self.photo_image)
