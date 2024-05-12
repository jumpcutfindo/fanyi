class Preset:
  def __init__(self, name, screen, left, top, width, height):
    self.name = name
    self.screen = screen
    self.left = left
    self.top = top
    self.width = width
    self.height = height

class PresetManager:
  def __init__(self):
    self.presets = []
    self.preset_map = {}

  def add_preset(self, name, screen, left, top, width, height):
    preset = Preset(name, screen, left, top, width, height)
    self.presets.append(preset)
    self.preset_map[name] = preset

    return preset

  def get_preset(self, name):
    return self.preset_map[name]

  def list_presets(self):
    return self.presets
  
  def delete_preset(self, name):
    self.presets.remove(self.get_preset(name))
    del self.preset_map[name]