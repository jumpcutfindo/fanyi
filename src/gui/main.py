import tkinter as tk

from controller import Controller
from preferences import PreferenceManager
from presets import PresetManager

from .menu import MenuFrameContainer
from .results import ResultFrameContainer

ORIGINAL_DPI = 95


class MainFrameContainer:
    def __init__(self, controller: Controller, preset_manager: PresetManager, preference_manager: PreferenceManager):
        self.controller = controller
        self.preset_manager = preset_manager
        self.preference_manager = preference_manager

        self.root = tk.Tk()
        self.root.title("Fanyi")

        # Scale according to current DPI
        self.scale = self.get_dpi() / ORIGINAL_DPI
        self.root.geometry(
            f"{self.scaled(800)}x{self.scaled(600)}")

        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.menu_frame = MenuFrameContainer(self)

        sep = tk.Frame(self.frame, width=2, bd=1, relief='sunken')
        sep.pack(side=tk.LEFT, fill=tk.Y)

        self.result_frame = ResultFrameContainer(self)

    def start(self):
        self.root.mainloop()

    def get_dpi(self):
        return self.root.winfo_fpixels('1i')

    def scaled(self, width):
        return round(width * self.scale)

    def get_controller(self):
        return self.controller

    def get_preset_manager(self):
        return self.preset_manager

    def get_preference_manager(self):
        return self.preference_manager
    
    def on_screenshot(self, preset):
        screenshots = self.controller.on_partial_capture(preset)
        return screenshots

    def on_screenshot_and_process(self, preset):
        screenshots = self.controller.on_partial_capture(preset)
        result = self.controller.process_image(screenshots)
        self.set_results(result)

    def set_results(self, results):
        filename, phrases = results
        self.result_frame.set_results(filename, phrases)
