from controller import Controller
from dictionary import parser


def main():
  print("Initializing application...")

  # TODO: Implement a way to manage this
  dictionary = parser.parse(
      './.cache/cedict_ts.u8')

  controller = Controller(dictionary)
  controller.start()


if __name__ == "__main__":
  main()
