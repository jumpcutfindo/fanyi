import tkinter as tk
from tkinter.filedialog import askopenfilename

class SettingsFrame:

  def __init__(self, root, options_frame):
    self.root = root
    self.options_frame = options_frame

    self.settings_frame = tk.Frame(self.options_frame)
    self.settings_frame.pack(side=tk.TOP, fill=tk.X)

    settings_label = tk.Label(self.settings_frame, text="Settings")
    settings_label.pack(side=tk.TOP, pady=[0, 8], anchor=tk.NW)

    self.__dictionary_source_setting()
    self.__language_setting()

  def __dictionary_source_setting(self):
    self.dictionary_source_frame = tk.Frame(self.settings_frame)
    self.dictionary_source_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=[0, 8])

    dictionary_source_label = tk.Label(self.dictionary_source_frame, text="Dictionary")
    dictionary_source_label.pack(side=tk.TOP, anchor=tk.NW)

    # Dictionary file input
    dictionary_source_input_frame = tk.Frame(self.dictionary_source_frame)
    dictionary_source_input_frame.pack(side=tk.TOP, fill=tk.X)
    
    self.dictionary_source_var = tk.StringVar(self.root, "dict_src")
    self.dictionary_source_var.set("<no dictionary selected>")  # Default selection
    dictionary_source_input = tk.Entry(self.dictionary_source_frame, textvariable=self.dictionary_source_var)
    dictionary_source_input.pack(side=tk.LEFT, fill=tk.X)

    dictionary_source_choose_file_btn = tk.Button(self.dictionary_source_frame, text="Choose File", command=self.__choose_dict_file)
    dictionary_source_choose_file_btn.pack(side=tk.LEFT)
  
  def __choose_dict_file(self):
    filename = askopenfilename()
    if filename:
      print(filename)
      self.dictionary_source_var.set(filename)

  def __language_setting(self):
    self.language_frame = tk.Frame(self.settings_frame)
    self.language_frame.pack(side=tk.TOP, fill=tk.BOTH, pady=[0, 8])

    language_label = tk.Label(self.language_frame, text="Language:")
    language_label.pack(side=tk.LEFT)
    
    language_var = tk.StringVar(self.root, "language")
    languages = ["Simplified Chinese", "Traditional Chinese"] # TODO: Add actual languages supported
    language_var.set(languages[0])  # Default selection
    language_dropdown = tk.OptionMenu(self.language_frame, language_var, *languages)
    language_dropdown.pack(side=tk.LEFT)