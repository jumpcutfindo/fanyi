import re


def __read_file(file_name: str) -> str:
  """Opens and reads the text within the provided file"""
  f = open(file_name, 'r', encoding='utf-8')
  return f.read()


def __remove_copyright(text: str) -> str:
  """Removes the chunk of copyright text present at the top of the dict file"""
  pattern = re.compile(r'^#.*\n', re.MULTILINE)
  return pattern.sub('', text)


def parse(file_name: str):
  """Parses the given dictionary file into an application friendly format"""
  print('Parsing Mandarin dictionary data...')
  raw_text = __read_file(file_name)
  raw_text = __remove_copyright(raw_text)

  print(raw_text)

  print('Dictionary parsed')
