from ctypes import windll

from controller import Controller
from presets import PresetManager

from gui.main import MainFrame

def main():
  print("Initializing application...")

  windll.shcore.SetProcessDpiAwareness(1)

  controller = Controller()
  preset_manager = PresetManager()

  gui = MainFrame(controller, preset_manager)
  gui.start()

  # TODO: Implement a way to manage this
  # dictionary = parser.parse(
  #     './.cache/cedict_ts.u8')

  # controller = Controller(dictionary)
  # controller.start()


if __name__ == "__main__":
  main()
