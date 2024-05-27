import tkinter as tk
from typing import TYPE_CHECKING

from .screenshot import ScreenshotFrameContainer
from .translations import TranslationsFrameContainer

if TYPE_CHECKING:
    from gui import MainFrameContainer


class ResultFrameContainer:
    def __init__(self, parent: "MainFrameContainer"):
        self.parent = parent

        self.frame = tk.Frame(parent.frame)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.screenshot_frame = ScreenshotFrameContainer(self)

        sep = tk.Frame(self.frame, height=2, bd=1, relief='sunken')
        sep.pack(side=tk.TOP, fill=tk.X)

        self.translation_frame = TranslationsFrameContainer(self)

    def set_results(self, filename, phrases):
        screenshot = filename
        self.screenshot_frame.set_screenshot(screenshot)
        self.translation_frame.set_translations(phrases)
