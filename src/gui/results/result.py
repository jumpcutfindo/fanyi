import tkinter as tk

from .screenshot import ScreenshotFrameContainer
from .translations import TranslationsFrameContainer


class ResultFrameContainer:
    def __init__(self, parent):
        self.parent = parent

        self.frame = tk.Frame(parent.frame, bd=1, relief=tk.SOLID)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.screenshot_frame = ScreenshotFrameContainer(self)
        self.translation_frame = TranslationsFrameContainer(self)

    def set_results(self, filenames, read_text, phrases):
        print(phrases)
