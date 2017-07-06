import numpy
import cv2
aa

def remove_page_grid(image):  # numpy.median is a function
    median_size = 7
    return_image = vertical_median_filter(image, median_size)
    return_image = horizontal_median_filter(return_image, median_size)
    return return_image


def vertical_median_filter(image, size):
    pass


def horizontal_median_filter(image, size):
    pass
