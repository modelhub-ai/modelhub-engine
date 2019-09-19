
from PIL import Image

from .imageLoader import ImageLoader


class PilImageLoader(ImageLoader):
    """
    Loads common 2d image formats (png, jpg, ...) using Pillow (PIL).
    """

    def _load(self, input):
        """
        Loads input using PIL.

        Args:
            input (str): Name of the input file to be loaded

        Returns:
            PIL.Image object
        """
        return Image.open(input)


    def _getImageDimensions(self, image):
        """
        Args:
            image (PIL.Image): Image as loaded by :func:`_load`

        Returns:
            Image dimensions from PIL image object
        """
        imageDims = [len(image.getbands())]
        imageDims.extend(list(image.size)[::-1])
        return imageDims
