from jdeskew.estimator import get_angle
from jdeskew.utility import rotate
from paddleocr import PaddleOCR
import math
from jdeskew.estimator import get_angle
from jdeskew.utility import rotate

def preprocess(image):

    angle = get_angle(image)
    output_image= rotate(image, angle)

    return output_image

def apply_ocr(ocr, image):

    output_image = preprocess(image)
    result = ocr.ocr(output_image)
    
    boxes = [line[0] for line in result[:][0]]
    txts = [line[1][0] for line in result[:][0]]
    scores = [line[1][1] for line in result[:][0]]

    return txts, boxes, scores

##Function to calculate euclidian distance
def euclidean_distance(centroid_1, centroid_2):
    
    x1, y1 = centroid_1
    x2, y2 = centroid_2
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    
    return distance

##Function to calculate centroid
def calculate_centroid(box):
    
    x_values = [point[0] for point in box]
    y_values = [point[1] for point in box]
    x_center = sum(x_values) / len(box)
    y_center = sum(y_values) / len(box)
    
    return (x_center, y_center)