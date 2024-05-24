import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.results.result import ResultFrameContainer


class TranslationsFrameContainer:
    def __init__(self, parent: "ResultFrameContainer"):
        self.parent = parent

        self.frame = tk.Frame(parent.frame)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(self.frame)
        scrollbar = tk.Scrollbar(
            self.frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.pack(side=tk.LEFT)

        canvas.create_window((0, 0), window=scrollable_frame,
                             anchor=tk.NW, tags=('canvas_frame'))
        canvas.bind('<Configure>', self.__handle_resize)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = canvas
        self.scrollable_frame = scrollable_frame

        self.table_widgets = []

    def __handle_resize(self, event):
        canvas = event.widget
        canvas.itemconfigure("canvas_frame", width=event.width)

        canvas.configure(scrollregion=canvas.bbox("all"))

        # Adjust wraplength of definition labels
        if self.table_widgets:
            for label in self.table_widgets:
                translation_frame, simplified_label, traditional_label, pinyin_label, definitions_label = label
                wraplength = translation_frame.winfo_width() - (simplified_label.winfo_width() +
                                                                traditional_label.winfo_width() + pinyin_label.winfo_width() + 128)
                definitions_label.configure(wraplength=wraplength)

    def set_translations(self, translations):
        self.table_widgets = []

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for index, (key, entries) in enumerate(translations.items()):
            containing_frame = tk.Frame(
                self.scrollable_frame, background='white')
            containing_frame.pack(fill=tk.X, pady=8, padx=8, expand=True)

            # Sentence
            key_label = tk.Label(
                containing_frame, text=key, font=('Microsoft Yahei', 14), background='white', justify='left', wraplength=self.scrollable_frame.winfo_width() - 32)
            key_label.pack(padx=8, pady=8, anchor=tk.W)

            # Bind sentence label to resize on window resize
            self.canvas.bind('<Configure>', lambda e: key_label.configure(
                wraplength=self.scrollable_frame.winfo_width() - 32), add=True)

            translation_frame = tk.Frame(
                containing_frame, background='white')
            translation_frame.pack(
                side=tk.TOP, fill=tk.X, padx=8, pady=8)
            translation_frame.columnconfigure(3, weight=1)

            if not entries or len(entries) == 0:
                not_exists_label = tk.Label(
                    translation_frame, text='No words found', font='Microsoft Yahei 10 italic', background='white')
                not_exists_label.grid(
                    row=0, column=0, padx=8, pady=8, sticky=tk.W)
                continue

            # Insert each entry as a line
            for index, entry in enumerate(entries):
                if not entry:
                    continue

                simplified_label = tk.Label(translation_frame, text=f'{entry.simplified}', font=(
                    'Microsoft Yahei', 10), background='white')
                simplified_label.grid(
                    row=index, column=0, padx=(0, 8), sticky=tk.NW)

                traditional_label = tk.Label(translation_frame, text=f'({entry.traditional})', font=(
                    'Microsoft Yahei', 10), background='white')
                traditional_label.grid(
                    row=index, column=1, padx=8, sticky=tk.NW)

                pinyin_label = tk.Label(translation_frame, text=f'{entry.pinyin}', font=(
                    'Microsoft Yahei', 10), background='white')
                pinyin_label.grid(row=index, column=2, padx=8, sticky=tk.NW)

                definitions = []
                for i, d in enumerate(entry.definitions):
                    definitions.append(f'{i+1}. {d}')
                definitions_label = tk.Label(translation_frame, font=(
                    'Microsoft Yahei', 10), text='\n'.join(definitions), background='white', justify='left', wraplength=300)

                definitions_label_padding_y = 16 if index < len(
                    entries) - 1 else 0

                definitions_label.grid(
                    row=index, column=3, padx=8, pady=(0, definitions_label_padding_y), sticky=tk.W)

                # Add labels to list for refresh calculations
                self.table_widgets.append(
                    (translation_frame, simplified_label, traditional_label, pinyin_label, definitions_label))
