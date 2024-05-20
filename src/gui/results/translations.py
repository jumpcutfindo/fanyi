import tkinter as tk


class TranslationsFrameContainer:
    def __init__(self, parent):
        self.parent = parent

        canvas = tk.Canvas(parent.frame)
        scrollbar = tk.Scrollbar(
            parent.frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.frame = scrollable_frame

    def set_translations(self, translations):
        for key, words in translations.items():
            frame = tk.Frame(self.frame, bd=1, relief=tk.SOLID)
            frame.pack(fill=tk.X, padx=5, pady=5)

            key_label = tk.Label(frame, text=key, font=('Arial', 12, 'bold'))
            key_label.pack(anchor=tk.W, padx=5, pady=2)

            for word in words:
                if not word:
                    continue

                traditional_label = tk.Label(
                    frame, text=f"Traditional: {word.traditional}", font=('Arial', 10))
                traditional_label.pack(anchor=tk.W, padx=20, pady=2)

                simplified_label = tk.Label(
                    frame, text=f"Simplified: {word.simplified}", font=('Arial', 10))
                simplified_label.pack(anchor=tk.W, padx=20, pady=2)

                pinyin_label = tk.Label(
                    frame, text=f"Pinyin: {word.pinyin}", font=('Arial', 10))
                pinyin_label.pack(anchor=tk.W, padx=20, pady=2)

                for definition in word.definitions:
                    definition_label = tk.Label(
                        frame, text=f"Definition: {definition}", font=('Arial', 10))
                    definition_label.pack(anchor=tk.W, padx=40, pady=2)
