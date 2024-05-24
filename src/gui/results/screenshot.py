import tkinter as tk
from PIL import ImageTk, Image
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.results.result import ResultFrameContainer


class ScreenshotFrameContainer:
    def __init__(self, parent: "ResultFrameContainer"):
        self.parent = parent

        self.frame = tk.Frame(parent.frame, height=240)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, padx=16)
        self.frame.grid_propagate(False)

        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.frame.bind('<Configure>', self.__handle_resize)

        title_frame = tk.Frame(self.frame)
        title_frame.grid(row=0, column=0, sticky=tk.NW)

        translations_label = tk.Label(
            title_frame, text="Screenshot", justify=tk.LEFT)
        translations_label.pack(side=tk.TOP, pady=8)

        self.image_label = tk.Label(
            self.frame, text='test')
        self.image_label.grid(sticky=tk.NSEW)

    def set_screenshot(self, src):
        self.screenshot = Image.open(src)
        self.__create_resized_image()

    def __create_resized_image(self):
        width, height = self.__get_scaled_size(
            self.frame.winfo_width(), self.frame.winfo_height(), self.screenshot.width, self.screenshot.height)

        self.photo_image = ImageTk.PhotoImage(
            self.screenshot.resize(size=(width, height)))

        self.image_label.configure(image=self.photo_image)

    def __handle_resize(self, event):
        if not self.screenshot:
            return

        self.__create_resized_image()

    def __get_scaled_size(self, frame_width, frame_height, width, height):
        ratio = min(frame_width / width, frame_height / height)
        return max(1, round(width * ratio)), max(1, round(height * ratio))
