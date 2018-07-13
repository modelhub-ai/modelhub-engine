import SimpleITK as sitk

from .imageLoader import ImageLoader


class SitkImageLoader(ImageLoader):
    """
    Loads image formatd supported by SimpleITK
    """

    def _load(self, input):
        return sitk.ReadImage(input)
    

    def _getImageDimensions(self, image):
        imageDims = list(image.GetSize())
        if len(imageDims) == 2:
            imageDims.append(1)
        imageDims = imageDims[::-1]
        return imageDims


