import smokesignal

from threading import Thread
from controller import Controller
from gui import MainFrameContainer
from presets import Preset

def init(c: Controller, g: MainFrameContainer):
    global controller
    global gui

    controller = c
    gui = g
    
@smokesignal.on('process_and_update')
def process_and_update(screenshot: str):
    if not gui:
        return

    def action():
        gui.set_processing(True)
        
        result = __process(screenshot)

        gui.set_results(None, result)

        gui.set_processing(False)

    thread = Thread(target=action)
    thread.start()

@smokesignal.on('screenshot_and_update')
def screenshot_and_update(preset: Preset):
    def action():
        gui.set_processing(True)
        
        screenshot = __screenshot(preset)
        result = __process(screenshot)

        gui.set_results(preset, result)

        gui.set_processing(False)

    thread = Thread(target=action)
    thread.start()

def __screenshot(preset: Preset):
    screenshot = controller.on_partial_capture(preset)
    return screenshot

def __process(screenshot: str):
    result = controller.process_image(screenshot)
    return result