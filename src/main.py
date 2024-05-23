from ctypes import windll

import sys
from loguru import logger

from controller import Controller
from presets.preset_manager import PresetManager
from files import FileManager
from preferences import PreferenceManager

from gui.main import MainFrameContainer


def main():
    # Setup logger version
    logger.remove()
    logger.add(
        sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <lvl>{message}</lvl>", level="DEBUG")
    logger.info("Initializing application...")

    # Setup logical part of application
    file_manager = FileManager()
    preset_manager = PresetManager(file_manager)
    preference_manager = PreferenceManager(file_manager)
    controller = Controller(file_manager, preference_manager)

    # Setup GUI stuff
    windll.shcore.SetProcessDpiAwareness(1)
    gui = MainFrameContainer(controller, preset_manager, preference_manager)

    # TODO: Remove this for testing
    results = controller.process_image(['.\\.cache\\screenshot.png'])
    gui.set_results(results)

    gui.start()


if __name__ == "__main__":
    main()
