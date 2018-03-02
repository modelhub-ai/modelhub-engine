import SimpleITK as sitk

from modelhublib.imageloaders import ImageLoader


class SitkImageLoader(ImageLoader):
    """
    Loads image formatd supported by SimpleITK
    """

    def _load(self, input):
        return sitk.ReadImage(input)
    

    def _checkConfigCompliance(self, image):
        limits = self._config["model"]["input"]["dim_limits"]
        imageDims = list(image.GetSize())
        if len(imageDims) == 2:
            imageDims.append(1)
        imageDims = imageDims[::-1]
        for i in range(3):
            if ((("min" in limits[i]) and (limits[i]["min"] > imageDims[i])) or
                (("max" in limits[i]) and (limits[i]["max"] < imageDims[i]))):
                raise IOError("Image dimensions %s do not comply with input requirements" % str(tuple(imageDims)))


