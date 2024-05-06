from easyocr import easyocr


def read_simplified(filename):
  reader = easyocr.Reader(['ch_sim', 'en'])
  return reader.readtext(filename, detail=0)


def read_traditional(filename):
  reader = easyocr.Reader(['ch_tra', 'en'])
  return reader.readtext(filename, detail=0)
