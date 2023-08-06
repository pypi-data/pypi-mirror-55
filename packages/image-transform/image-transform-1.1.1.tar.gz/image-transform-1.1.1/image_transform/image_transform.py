"""image_transform."""
import PIL
from PIL import Image

class ImageTransform:
    """Image processing helper."""

    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path)

    def scale(self, scale_size=256):
        """
        scale an image by resizing its shortest side to the given scale_size,
        and keeping its aspect ratio.
        """
        width, height = self.image.size
        resized_width = scale_size
        resized_height = scale_size
        if width >= height:
            height_percent = (scale_size / float(height))
            resized_width = int((float(width) * float(height_percent)))
        else:
            width_percent = (scale_size / float(width))
            resized_height = int((float(height) * float(width_percent)))

        img = self.image.resize((resized_width, resized_height), PIL.Image.ANTIALIAS)

        return img

    def center_crop(self, size=224):
        """
        crop an image from the center by the given size.
        """
        width, height = self.image.size
        (left, upper, right, lower) = (
            (width - size)/2,
            (height - size)/2,
            (width + size)/2,
            (height + size)/2
        )
        img = self.image.crop((left, upper, right, lower))

        return img

    def horizontal_flip(self):
        """
        horizontally flip an image.
        """
        img = self.image.transpose(PIL.Image.FLIP_TOP_BOTTOM)

        return img
