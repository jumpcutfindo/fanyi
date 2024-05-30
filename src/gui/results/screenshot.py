import tkinter as tk
from PIL import ImageTk, Image
from typing import TYPE_CHECKING

from gui.utils import get_scaled_size

if TYPE_CHECKING:
    from gui import MainFrameContainer
    from gui.results import ResultFrameContainer


class ScreenshotFrameContainer: 
    def __init__(self, root: "MainFrameContainer", parent: "ResultFrameContainer"):
        self.root = root
        self.parent = parent

        self.preset = None
        self.screenshot_src = None
        self.screenshot = None

        self.frame = tk.Frame(parent.frame, height=240)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, padx=8)
        self.frame.grid_propagate(False)

        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.frame.bind('<Configure>', self.__handle_resize)

        title_frame = tk.Frame(self.frame)
        title_frame.grid(row=0, column=0, sticky=tk.NW)

        self.translations_label = tk.Label(
            title_frame, text="Screenshot", justify=tk.LEFT)
        self.translations_label.pack(side=tk.TOP, pady=8)

        self.image_label = tk.Label(self.frame, cursor='hand1')
        self.image_label.grid(sticky=tk.NSEW)

    def set_screenshot(self, preset, src):
        if self.preset:
            self.preset = preset
            
            # Set the label to include preset name
            self.translations_label.configure(text=f'Screenshot ({self.preset.name})')

        self.screenshot_src = src
        self.screenshot = Image.open(src)

        # Set the label to include preset name
        self.translations_label.configure(text=f'Screenshot ({self.preset.name})')
        
        self.__configure_resized_image()

    def __configure_resized_image(self):
        if not self.screenshot:
            return

        width, height = get_scaled_size(
            self.frame.winfo_width(), self.frame.winfo_height(), self.screenshot.width, self.screenshot.height)

        self.photo_image = ImageTk.PhotoImage(
            self.screenshot.resize(size=(width, height)))

        self.image_label.configure(image=self.photo_image)
        self.image_label.bind("<Button-1>", self.__open_image_preview)

    def __handle_resize(self, event):
        if not self.screenshot:
            return

        self.__configure_resized_image()

    def __open_image_preview(self, event):
        if not self.screenshot or not self.screenshot_src:
            return
        
        if not self.preset:
            title = f'{self.screenshot_src} (No preset used)'
        else:
            title = f'{self.screenshot_src} (L: {self.preset.left}; T: {self.preset.top}; W: {self.preset.width}; H: {self.preset.height})'

        self.root.show_screenshot_preview(title, self.screenshot_src)
