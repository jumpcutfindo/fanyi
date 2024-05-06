import mss
from datetime import datetime


def take_full_screenshot():
  sct = mss.mss()
  filenames = sct.save(
      mon=-1, output="{dt}_all-monitors".format(dt=__get_screenshot_name()))

  return filenames


def take_monitor_screenshot(monitor):
  sct = mss.mss()
  filenames = sct.save(
      mon=monitor, output="{dt}_monitor-{mon}".format(dt=__get_screenshot_name(), mon=monitor))

  return filenames


def __get_screenshot_name():
  return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
