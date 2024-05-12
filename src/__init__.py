from controller import Controller
from dictionary import parser

from gui.main import MainFrame

def main():
  print("Initializing application...")

  controller = Controller()

  gui = MainFrame(controller)
  gui.start()

  # TODO: Implement a way to manage this
  # dictionary = parser.parse(
  #     './.cache/cedict_ts.u8')

  # controller = Controller(dictionary)
  # controller.start()


if __name__ == "__main__":
  main()
