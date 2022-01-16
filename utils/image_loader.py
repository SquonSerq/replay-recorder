from PIL import Image, ImageTk


class ImageLoader:
    def __init__(self, path):
        self.image = Image.open(path)

    def get_tkinter_image(self, x, y):
        return ImageTk.PhotoImage(self.image.resize((x, y)))