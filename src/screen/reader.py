from easyocr import easyocr


def read_simplified(filename):
  print('Attempting to read Simplified Chinese...')
  reader = easyocr.Reader(['ch_sim'])
  return reader.readtext(filename, detail=0)


def read_traditional(filename):
  print('Attempting to read Traditional Chinese...')
  reader = easyocr.Reader(['ch_tra'])
  return reader.readtext(filename, detail=0)
