import SimpleITK as sitk

from .imageLoader import ImageLoader


class SitkImageLoader(ImageLoader):
    """
    Loads image formats supported by SimpleITK
    """

    def _load(self, input):
        """
        Loads input using SimpleITK.

        Args:
            input (str): Name of the input file to be loaded

        Returns:
            SimpleITK.Image object
        """
        return sitk.ReadImage(input)


    def _getImageDimensions(self, image):
        """
        Args:
            image (SimpleITK.Image): Image as loaded by :func:`_load`

        Returns:
            Image dimensions from SimpleITK image object
        """
        imageDims = list(image.GetSize())
        if len(imageDims) == 2:
            imageDims.append(1)
        imageDims = imageDims[::-1]
        return imageDims
