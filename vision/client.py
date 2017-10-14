import requests
import json
import cv2
from PIL import Image
from StringIO import StringIO
import numpy as np
from color.nrp_project import ShapeAlphaColorClassifier

classifier = ShapeAlphaColorClassifier.default("color/train/color_data.csv")

def get_next_image(url):
    next_image = json.loads(requests.get("http://{}/next-image".format(url)).content)["img_name"]
    img_data = requests.get("http://{}/get-image/{}".format(url, next_image))
    img_buffer = StringIO(img_data.content)
    img_array = np.asarray(bytearray(img_buffer.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, 1)
    return next_image, img


def return_image_color(url, image_name, shape_color, alpha_color):
    content = {"shape_color" : shape_color, "alpha_color" : alpha_color}
    requests.post("http://{}/classify/{}".format(url, image_name), params=content)

def do_classify(url):
    image_name, img = get_next_image(url)
    shape_color, alpha_color = classifier.get_color(img)
    return_image_color(url, image_name, shape_color, alpha_color)


if __name__ == "__main__":
    do_classify("localhost:5000")