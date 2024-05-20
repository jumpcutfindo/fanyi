import tkinter as tk

from .menu.menu import MenuFrameContainer
from .result import ResultFrameContainer

ORIGINAL_DPI = 95


class MainFrameContainer:
    def __init__(self, controller, preset_manager):
        self.controller = controller
        self.preset_manager = preset_manager

        self.root = tk.Tk()
        self.root.title("Fanyi")

        # Scale according to current DPI
        self.scale = self.get_dpi() / ORIGINAL_DPI
        self.root.geometry(f"{self.scaled(800, self.scale)}x{
                           self.scaled(600, self.scale)}")

        self.frame = tk.Frame(self.root, bd=1, relief=tk.SOLID)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.menu_frame = MenuFrameContainer(self)
        self.result_frame = ResultFrameContainer(self)

    def start(self):
        self.root.mainloop()

    def get_dpi(self):
        return self.root.winfo_fpixels('1i')

    def scaled(self, width, scale):
        return round(width * scale)

    def get_preset_manager(self):
        return self.preset_manager

    def get_controller(self):
        return self.controller

    def on_screenshot(self, preset):
        result = self.controller.on_partial_screenshot(preset)
