from PIL import Image

from modelhublib.imageloaders import ImageLoader


class PilImageLoader(ImageLoader):
    """
    Loads common 2d image formats (png, jpg, ...) using Pillow (PIL).
    """
    
    def _load(self, input):
        return Image.open(input)


    def _getImageDimensions(self, image):
        imageDims = [len(image.getbands())]
        imageDims.extend(list(image.size)[::-1])
        return imageDims
