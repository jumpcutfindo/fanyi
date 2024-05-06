from input import listener


def on_request_capture():
  print('Capture requested')


def on_exit(il):
  print('Exiting application')
  il.stop()


def main():
  print("Initializing application...")

  il = listener.InputListener()
  il.register_hotkey('request_capture', '<ctrl>+<alt>+h', on_request_capture)
  il.register_hotkey('exit', '<ctrl>+<alt>+j', lambda: on_exit(il))

  il.start()

  print("Application initialized")


if __name__ == "__main__":
  main()
