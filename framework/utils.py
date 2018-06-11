from datetime import datetime
import json
import os

from PIL import Image



# ALLOWED_EXTENSIONS = json.load(open("model/config.json"))['model']['input']['format']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def save_uploaded_file(file, folder):
    """
    Saves the uploaded input file to the given folder and returns the path.
    """
    now = datetime.now()
    filename = os.path.join(folder,
    "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"),
    file.filename.rsplit('.', 1)[1]))
    file.save(filename)
    return filename

def process_predicted_image(image):
    """
    Changes all white pixels to yellow, and all black to transparent.
    Uses crude nested loop - to be optimized.
    Assumes that ROI is white & background is black,
    Assumes predicted image is RGBA
    """
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if  120 < pixels[i,j][0] and pixels[i,j][0] < 256:
               pixels[i,j] = (255,171,64,190)
            else:
               pixels[i,j] = (0,0,0,0)
    return image

def save_predicted_image(image, folder):
    """
    Saves the predicted image to the given folder and returns the path.
    """
    now = datetime.now()
    filename = os.path.join(folder,
    "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"),
    "png"))
    image = process_predicted_image(image)
    image.save(filename)
    return filename

def sort_result_type(result, folder, input):
    """
    Returns a json object depending on the type of object returned from
    the inference function. Only check for images.
    """
    if isinstance(result, Image.Image):
        filename = save_predicted_image(result, folder)
        result = jsonify(type='image',result=filename, input=input)
    else:
        result = jsonify(type='probabilities',result=result, input=input)
    return result
