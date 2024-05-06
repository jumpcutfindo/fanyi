import mss


def take_full_screenshot():
  sct = mss.mss()
  filenames = sct.save()

  return filenames
