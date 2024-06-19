from threading import Thread
from controller import Controller
from gui import MainFrameContainer
from presets import Preset


# The Coordinator class intends to act as an in-between for the Controller and GUI.
# Functionality that requires the coordination between these two classes should be implemented here.
class Coordinator:
    def __init__(self, controller: Controller, gui: MainFrameContainer):
        self.controller = controller
        self.gui = gui
    
    def process_and_update(self, preset: Preset, screenshot: str):
        def action():
            self.gui.set_processing(True)
            
            result = self.__process(screenshot)

            self.gui.set_results(preset, result)

            self.gui.set_processing(False)

        thread = Thread(target=action)
        thread.start()

    def screenshot_and_update(self, preset: Preset):
        def action():
            self.gui.set_processing(True)
            
            screenshot = self.__screenshot(preset)
            result = self.__process(screenshot)

            self.gui.set_results(preset, result)

            self.gui.set_processing(False)

        thread = Thread(target=action)
        thread.start()

    def __screenshot(self, preset: Preset):
        screenshot = self.controller.on_partial_capture(preset)
        return screenshot
    
    def __process(self, screenshot: str):
        result = self.controller.process_image(screenshot)
        return result