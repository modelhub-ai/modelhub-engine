from datetime import datetime
import json
import os

ALLOWED_EXTENSIONS = json.load(open("model/config.json"))['model']['input']['format']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def saveUploadedFile(file, folder):
    """
    Saves the uploaded input file to the given folder and returns the path.
    """
    now = datetime.now()
    filename = os.path.join(folder,
    "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"),
    file.filename.rsplit('.', 1)[1]))
    file.save(filename)
    return filename

def savePredictedImage(Image, folder):
    """
    Saves the predicted image to the given folder and returns the path.
    """
    now = datetime.now()
    filename = os.path.join(folder,
    "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"),
    "jpg"))
    Image.save(filename)
    return filename
