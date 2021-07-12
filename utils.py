import os
from local_settings import PATH


def getImagePath(image):
    return os.path.join(PATH, 'img', image)
