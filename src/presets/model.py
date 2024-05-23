class Preset:
    def __init__(self, name: str, screen: int, left: int, top: int, width: int, height: int):
        self.name = name
        self.screen = screen
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    @staticmethod
    def from_json(json):
        return Preset(json['name'], json['screen'], json['left'], json['top'], json['width'], json['height'])
