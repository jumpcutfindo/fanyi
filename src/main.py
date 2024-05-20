from ctypes import windll

from controller import Controller
from presets import PresetManager
from files import FileManager

from gui.main import MainFrameContainer


def main():
    print("Initializing application...")

    windll.shcore.SetProcessDpiAwareness(1)

    file_manager = FileManager()
    preset_manager = PresetManager(file_manager)
    controller = Controller(file_manager)

    gui = MainFrameContainer(controller, preset_manager)
    gui.start()

    # TODO: Implement a way to manage this
    # dictionary = parser.parse(
    #     './.cache/cedict_ts.u8')

    # controller = Controller(dictionary)
    # controller.start()


if __name__ == "__main__":
    main()
