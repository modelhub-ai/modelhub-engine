from PIL import Image

from modelhublib.imageloaders import ImageLoader


class PilImageLoader(ImageLoader):
    """
    Loads common 2d image formats (png, jpg, ...) using Pillow (PIL).
    """
    
    def _load(self, input):
        return Image.open(input)


    def _checkConfigCompliance(self, image):
        limits = self._config["model"]["input"]["dim_limits"]
        imageDims = [len(image.getbands())]
        imageDims.extend(list(image.size)[::-1])
        for i in range(3):
            if ((("min" in limits[i]) and (limits[i]["min"] > imageDims[i])) or
                (("max" in limits[i]) and (limits[i]["max"] < imageDims[i]))):
                raise IOError("Image dimensions %s do not comply with input requirements" % str(tuple(imageDims)))

