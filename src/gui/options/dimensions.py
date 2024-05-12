import tkinter as tk

class DimensionsFrame:
  def __init__(self, root, options_frame):
    self.root = root
    self.options_frame = options_frame

    self.dimensions_frame = tk.Frame(self.options_frame)
    self.dimensions_frame.pack(side=tk.TOP, fill=tk.BOTH)

    self.__add_dimension_configuration_frame()
    self.__dimension_preset_list_frame()

  def __add_dimension_configuration_frame(self):
    # Dimension configuration frame
    self.dimension_configuration_frame = tk.Frame(self.dimensions_frame)
    self.dimension_configuration_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    dimension_configuration_label = tk.Label(self.dimension_configuration_frame, text="Dimensions")
    dimension_configuration_label.pack(side=tk.TOP, pady=[0, 8], anchor=tk.NW)

    # Screen settings
    self.screen_value_frame = tk.Frame(self.dimension_configuration_frame)
    self.screen_value_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=[0, 8])

    screen_value_label = tk.Label(self.screen_value_frame, text="Screen:")
    screen_value_label.pack(side=tk.LEFT)

    screen_value_var = tk.StringVar(self.root)
    screens = ["Primary", "Secondary"] # TODO: Pull screen information from OS
    screen_value_var.set(screens[0])  # Default selection
    screen_dropdown = tk.OptionMenu(self.screen_value_frame, screen_value_var, *screens)
    screen_dropdown.pack(side=tk.LEFT)

    # Dimensions settings (top, left, height, width)
    # TODO: Populate the values with default screen vars
    self.dimension_values_frame = tk.Frame(self.dimension_configuration_frame)
    self.dimension_values_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=[0, 8])

    top_value_var = tk.IntVar(self.root)
    top_value_var.set(0)
    top_label = tk.Label(self.dimension_values_frame, text="T:")
    top_label.pack(side=tk.LEFT)
    top_value_input = tk.Entry(self.dimension_values_frame, textvariable=top_value_var, width=5)
    top_value_input.pack(side=tk.LEFT, padx=[0, 4])

    left_value_var = tk.IntVar(self.root)
    left_value_var.set(0)
    left_label = tk.Label(self.dimension_values_frame, text="L:")
    left_label.pack(side=tk.LEFT)
    left_value_input = tk.Entry(self.dimension_values_frame, textvariable=left_value_var, width=5)
    left_value_input.pack(side=tk.LEFT, padx=[0, 4])

    height_value_var = tk.IntVar(self.root)
    height_value_var.set(0)
    height_label = tk.Label(self.dimension_values_frame, text="H:")
    height_label.pack(side=tk.LEFT)
    height_value_input = tk.Entry(self.dimension_values_frame, textvariable=height_value_var, width=5)
    height_value_input.pack(side=tk.LEFT, padx=[0, 4])

    width_value_var = tk.IntVar(self.root)
    width_value_var.set(0)
    width_label = tk.Label(self.dimension_values_frame, text="W:")
    width_label.pack(side=tk.LEFT)
    width_value_input = tk.Entry(self.dimension_values_frame, textvariable=width_value_var, width=5)
    width_value_input.pack(side=tk.LEFT, padx=[0, 4])
    
    pass

  def __dimension_preset_list_frame(self):
    self.preset_list_frame = tk.Frame(self.options_frame)
    self.preset_list_frame.pack(side=tk.TOP, fill=tk.BOTH)

    preset_list_label = tk.Label(self.preset_list_frame, text="Presets")
    preset_list_label.pack(side=tk.TOP, pady=[0, 8], anchor=tk.NW)

    preset_list = tk.Listbox(self.preset_list_frame)
    preset_list.insert(0, "Preset 1")

    preset_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)