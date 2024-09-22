import json
import tkinter as tk
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from gui.results import ResultFrameContainer


class TranslationsFrameContainer:
    def __init__(self, parent: "ResultFrameContainer"):
        self.parent = parent
        self.current_translations = None

        self.frame = tk.Frame(parent.frame)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.__setup_title_frame()
        self.__setup_side_frame()
        self.__setup_scrollable_frame()

    def __setup_title_frame(self):
        title_frame = tk.Frame(self.frame)
        title_frame.pack(side=tk.TOP, anchor=tk.NW, padx=8, fill=tk.BOTH)

        translations_label = tk.Label(
            title_frame, text="Translations", justify=tk.LEFT, pady=8)
        translations_label.pack(side=tk.LEFT, pady=8)

        copy_to_clipboard_button = tk.Button(
            title_frame, text="Copy to Clipboard", justify=tk.RIGHT, command=self.__copy_translations_to_clipboard, 
        )
        copy_to_clipboard_button.pack(side=tk.RIGHT, pady=8)
    
    def __setup_side_frame(self):
        self.side_frame_width = 300
        self.side_frame = tk.Frame(self.frame, width=self.side_frame_width)
        self.side_frame.pack(side=tk.LEFT, anchor=tk.NW, padx=8, fill=tk.BOTH)
    
    def __setup_scrollable_frame(self):
        self.canvas = tk.Canvas(self.frame)
        self.canvas.bind("<Configure>", self.__handle_resize)

        # Setup scrollbar
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        
        # Setup scrollable frame
        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        
        self.scrollable_frame.bind('<Enter>', self.__bind_to_mousewheel)
        self.scrollable_frame.bind('<Leave>', self.__unbind_to_mousewheel)
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW, tags=('canvas_frame'))

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Setup other widgets
        self.table_widgets = []
        self.sentence_labels = []
        self.all_simplified_words_to_pos_map = {}


    def __set_translations_visible(self, is_visible):
        if is_visible:
            self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        else:
            self.frame.pack_forget()


    def __handle_resize(self, event):
        canvas = event.widget
        canvas.itemconfigure("canvas_frame", width=event.width)

        canvas.configure(scrollregion=canvas.bbox("all"))

        # Adjust wraplength of definition labels
        if self.table_widgets:
            for label in self.table_widgets:
                translation_frame, simplified_label, traditional_label, pinyin_label, definitions_label = label
                wraplength = translation_frame.winfo_width() - (simplified_label.winfo_width() +
                                                                traditional_label.winfo_width() + pinyin_label.winfo_width() + 160)
                definitions_label.configure(wraplength=wraplength)

        # Adjust wraplength of sentence labels
        if self.sentence_labels:
            for label in self.sentence_labels:
                label.configure(
                    wraplength=self.scrollable_frame.winfo_width() - 32)

    def set_translations(self, translations):
        self.__set_translations_visible(False)

        # Reset canvas scroll
        self.canvas.yview_moveto(0)

        self.table_widgets = []

        self.label_map = {}
        self.current_selected_simplified = None
        
        self.sentence_labels = []
        self.all_simplified_words_to_pos_map = {}

        self.current_translations = translations

        containing_frames = []

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Offset for tracking what y-pos we're currently at
        current_y_offset = 0
        for index, (key, entries) in enumerate(translations.items()):
            containing_frame = tk.Frame(
                self.scrollable_frame, background='white')
            containing_frame.pack(fill=tk.X, pady=4, padx=8, expand=True)

            containing_frames.append(containing_frame)

            # Sentence
            sentence_label = tk.Label(
                containing_frame, text=key, font=('Microsoft Yahei', 15), background='white', justify='left', wraplength=self.scrollable_frame.winfo_width() - 32)
            sentence_label.pack(padx=8, pady=8, anchor=tk.W)
            self.sentence_labels.append(sentence_label)

            # Translations, holds each entry and details
            translation_frame = tk.Frame(
                containing_frame, background='white')
            translation_frame.pack(
                side=tk.TOP, fill=tk.X, padx=8, pady=8)
            translation_frame.columnconfigure(3, weight=1)

            if not entries or len(entries) == 0:
                not_exists_label = tk.Label(
                    translation_frame, text='No words found', font=('Microsoft Yahei', 12, 'italic'), background='white')
                not_exists_label.grid(
                    row=0, column=0, padx=8, pady=8, sticky=tk.W)
                continue

            # Insert each entry as a line
            entry_y_offset = 0
            for index, entry in enumerate(entries):
                if not entry:
                    continue

                simplified_label = tk.Label(translation_frame, text=f'{entry.simplified}', font=(
                    'Microsoft Yahei', 12), background='white')
                simplified_label.grid(
                    row=index, column=0, padx=(0, 8), sticky=tk.NW)

                traditional_label = tk.Label(translation_frame, text=f'({entry.traditional})', font=(
                    'Microsoft Yahei', 12), background='white')
                traditional_label.grid(
                    row=index, column=1, padx=8, sticky=tk.NW)

                pinyin_label = tk.Label(translation_frame, text=f'{entry.pinyin}', font=(
                    'Microsoft Yahei', 12), background='white')
                pinyin_label.grid(row=index, column=2, padx=8, sticky=tk.NW)

                definitions = []
                for i, d in enumerate(entry.definitions):
                    definitions.append(f'{i+1}. {d}')
                definitions_label = tk.Label(translation_frame, font=(
                    'Microsoft Yahei', 12), text='\n'.join(definitions), background='white', justify='left', wraplength=300)

                definitions_label_padding_y = 16 if index < len(
                    entries) - 1 else 0

                definitions_label.grid(
                    row=index, column=3, padx=8, pady=(0, definitions_label_padding_y), sticky=tk.W)

                # Add labels to list for refresh calculations
                self.table_widgets.append(
                    (translation_frame, simplified_label, traditional_label, pinyin_label, definitions_label))
                
                # Add to simplified label map
                if entry.simplified not in self.label_map:
                    self.label_map[entry.simplified] = (simplified_label, traditional_label, pinyin_label, definitions_label)

                translation_frame.update_idletasks()
                entry_y_offset = translation_frame.winfo_height()

                # Add simplified word to map with its y-pos
                # We use only the first entry's y-pos for simplicity
                if entry.simplified not in self.all_simplified_words_to_pos_map:
                    self.all_simplified_words_to_pos_map[entry.simplified] = current_y_offset + entry_y_offset
                
            self.scrollable_frame.update_idletasks()
            current_y_offset = self.scrollable_frame.winfo_height() + len(entries) * 20

        # Adjust positions to proportional of height
        final_scrollable_height = self.scrollable_frame.winfo_height()
        for key in self.all_simplified_words_to_pos_map.keys():
            self.all_simplified_words_to_pos_map[key] = float(self.all_simplified_words_to_pos_map[key]) / float(final_scrollable_height)

        # Populate side frame

        # Delete all widgets in side frame
        for widget in self.side_frame.winfo_children():
            widget.destroy()

        side_frame_line = tk.Frame(self.side_frame)

        # Function for scrolling to a specific word at its y-pos
        def scroll_to_word(word):
            def internal_func():
                if self.current_selected_simplified:
                    for label in self.label_map[self.current_selected_simplified]:
                        label.config(bg="white")

                self.current_selected_simplified = word
                for label in self.label_map[word]:
                        label.config(bg="yellow")
                self.__scroll_to_y_pos(self.all_simplified_words_to_pos_map[word])
            return internal_func

        for word in self.all_simplified_words_to_pos_map.keys():
            side_frame_line.update_idletasks()

            simplified_button = tk.Button(side_frame_line, text=word, font=('Microsoft Yahei', 10), command=scroll_to_word(word))

            simplified_button_width = simplified_button.winfo_reqwidth()
            side_frame_line_width = side_frame_line.winfo_reqwidth()

            if side_frame_line_width + simplified_button_width > self.side_frame_width:
                # Length of line is too long, create new line
                side_frame_line.pack(side=tk.TOP, anchor=tk.NW, pady=2)

                side_frame_line = tk.Frame(self.side_frame)
                simplified_button = tk.Button(side_frame_line, text=word, font=('Microsoft Yahei', 10), command=scroll_to_word(word))

            simplified_button.pack(side=tk.LEFT, padx=1, pady=1)
        
        # Handle final side_frame_line
        if side_frame_line.winfo_reqwidth() > 0:
            side_frame_line.pack(side=tk.TOP, anchor=tk.NW, pady=2)

        self.__set_translations_visible(True)

    def __scroll_to_y_pos(self, y_pos):
        self.canvas.yview_moveto(y_pos)

    def __bind_to_mousewheel(self, event):
        self.canvas.bind_all('<MouseWheel>', self.__on_mousewheel)

    def __unbind_to_mousewheel(self, event):
        self.canvas.unbind_all('<MouseWheel>')

    def __on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def __copy_translations_to_clipboard(self):
        if not self.current_translations:
            return

        # Convert to full chunk of text
        text = '; '.join(list(self.current_translations.keys()))

        r = tk.Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(text)
        r.update()
        r.destroy()

        logger.info('Copied translations to clipboard')

