import mss
import mss.tools
from datetime import datetime


def take_full_screenshot():
  print('Taking full screenshot...')
  sct = mss.mss()
  filenames = list(sct.save(
      mon=-1, output="{dt}_all-monitors.png".format(dt=__get_screenshot_name())))
  print('Took the following screenshot(s): {}'.format(filenames))

  return filenames


def take_monitor_screenshot(monitor):
  print('Taking monitor {} screenshot...'.format(monitor))
  sct = mss.mss()
  filenames = sct.save(
      mon=monitor, output="{dt}_monitor-{mon}.png".format(dt=__get_screenshot_name(), mon=monitor))

  print('Took the following screenshot(s): {}'.format(filenames))

  return filenames


def get_monitors():
  sct = mss.mss()
  return sct.monitors


def take_partial_screenshot(params):
  print('Taking partial screenshot with params: {}'.format(params))
  sct = mss.mss()

  filename = "{dt}_partial.png".format(dt=__get_screenshot_name())

  sct_img = sct.grab(params)

  mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)

  print('Took the following screenshot(s): {}'.format([filename]))

  return [filename]


def __get_screenshot_name():
  return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
