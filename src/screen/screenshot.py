import mss
import mss.tools
from datetime import datetime
from loguru import logger

def take_full_screenshot(save_location):
    logger.info('Taking full screenshot...')

    filename = f'{save_location}\\{__get_screenshot_name()}_all-monitors.png'

    sct = mss.mss()
    filenames = list(sct.save(mon=-1, output=filename))
    logger.info('Took the following screenshot(s): {}'.format(filenames))

    return filenames


def take_monitor_screenshot(save_location, monitor):
    logger.info('Taking monitor {} screenshot...'.format(monitor))

    filename = f'{save_location}\\{
        __get_screenshot_name()}_monitor-{monitor}.png'

    sct = mss.mss()
    filenames = sct.save(mon=monitor, output=filename)

    logger.info('Took the following screenshot(s): {}'.format(filenames))

    return filenames

def take_partial_screenshot(save_location, params):
    logger.info('Taking partial screenshot with params: {}'.format(params))

    filename = f'{save_location}\\{__get_screenshot_name()}_partial.png'

    sct = mss.mss()
    sct_img = sct.grab(params)

    mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)

    logger.info('Took the following screenshot: {}'.format(filename))

    return filename

def get_monitors():
    sct = mss.mss()
    return sct.monitors

def __get_screenshot_name():
    return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
