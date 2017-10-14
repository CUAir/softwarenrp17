from termcolor import colored
import csv
import cv2
from segmentation import Segmenter
from color_classifier import ColorClassifier


def get_color_training_data(path):
    training_data = []
    with open(path, "rb") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            color_val = map(lambda x: int(x), row[0:3])
            color_name = row[3]
            training_data.append((color_val, color_name))
    return training_data


def get_testing_data(path):
    testing_data = []
    with open(path, "rb") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            img_name = row[0]
            shape_color = row[1]
            alpha_color = row[2]
            testing_data.append((img_name, (shape_color, alpha_color)))
    return testing_data


class ShapeAlphaColorClassifier(object):
    def __init__(self, color_classifier, segmenter):
        self.color_classifier = color_classifier
        self.segmenter = segmenter

    @staticmethod
    def default(train_path):
        color_training = get_color_training_data(train_path)
        color_classifier = ColorClassifier(color_training)
        shape_segmenter = Segmenter()
        classifier = ShapeAlphaColorClassifier(color_classifier, shape_segmenter)
        return classifier

    def get_color(self, img):
        shape_cval, alpha_cval = self.segmenter.segment_image(img)
        shape_color = self.color_classifier.classify(shape_cval)
        alpha_color = self.color_classifier.classify(alpha_cval)
        return shape_color, alpha_color



if __name__ == "__main__":
    shape_alpha_classifier = ShapeAlphaColorClassifier.default("train/color_data.csv")
    num_failed = 0
    for img_name, color in get_testing_data("test/test_data.csv"):
        pred_color = shape_alpha_classifier.get_color(cv2.imread("test/data/img_name"+".jpg"))
        if pred_color == color:
            print colored('passed case {}'.format(img_name), 'green')
        else:
            print colored('failed case {}: got {} was expecting {}'.format(img_name, pred_color, color), 'red')
            num_failed += 1

    if num_failed == 0:
        result = colored('passed all cases', 'green')
    else:
        result = colored('failed {} cases'.format(str(num_failed)), 'red')
    print "results: {}".format(result)
