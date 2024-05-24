# Fanyi (翻译)
![image](https://github.com/lancopku/pkuseg-python/assets/28668883/5fec00bd-cab7-4f82-9deb-1567e50bfce6)

Fanyi (翻译) is a simple, optical screen reading (OCR) application that is meant to aid in translating Mandarin content on the screen into English.

It uses the [CEDICT](https://en.wikipedia.org/wiki/CEDICT) dictionary to provide definitions for Chinese phrases and words.

Note: This has been developed and tested primarily on Windows systems

# How it works
The application takes a screenshot and passes it into [EasyOCR](https://github.com/JaidedAI/EasyOCR). The text is read, then passed into [pkuseg](https://github.com/lancopku/pkuseg-python) for Chinese word segmentation. The system then tries to map it to the parsed CEDICT and produces the result.

# Features
- Reads text on your screen and helps to translate between Simplified and Traditional Chinese into English
- Dictionary features that provide translations and pinyin
- Presets can be set up to easily capture the same region of the screen
- User interface for looking through information captured from the image provided
- User preferences for easy reuse on the next startup


# How to use
1. Ensure you have Python (>=3.12 preferrably) installed on your system
2. Install the required packages with `python -m pip install -r requirements.txt`
3. Launch the application
4. Select a valid CEDICT dictionary on your system
5. Select a preferred language
6. Set up a preset to define the boundaries of the screen capture
7. Screenshot, and let the system run :)

Note: By default, the installation will install a version of PyTorch that uses the CPU to carry out the screen reading. If you have an NVIDIA GPU, you might want to consider installing a version that supports CUDA. See the [PyTorch - Get Started](https://pytorch.org/get-started/locally/) page for more information.