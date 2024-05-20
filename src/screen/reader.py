from easyocr import easyocr
from loguru import logger


def read_simplified(filename):
    logger.info('Attempting to read Simplified Chinese...')
    reader = easyocr.Reader(['ch_sim'])
    return reader.readtext(filename, detail=0)


def read_traditional(filename):
    logger.info('Attempting to read Traditional Chinese...')
    reader = easyocr.Reader(['ch_tra'])
    return reader.readtext(filename, detail=0)
