import numpy
import cv2
from copy import copy


def remove_page_grid(image):  # numpy.median is a function
    median_size = 7
    return_image = vertical_median_filter(image, median_size)
    return_image = horizontal_median_filter(return_image, median_size)
    return return_image


def vertical_median_filter(image, size):
    size = (size - 1) / 2
    image_copy = copy(image)
    re_median_arr = numpy.zeros((len(image), len(image[0])))
    print len(image_copy[0])
    for i, line in enumerate(image):
        image_copy[i] = copy(image[i]) + copy(image[i]) + copy(image[i])
    print len(image_copy[0])
    index = len(image[0])

    for i in range(len(image)):
        for j in range(index, 2*index):
            temp = image_copy[i][j - size:j + 1 + size]
            print temp
            re_median_arr[i][j-index-1] = sorted(temp)[len(temp)/2][0]

    return re_median_arr


def horizontal_median_filter(image, size):
    size = (size - 1) / 2
    image_copy = copy(image)
    re_median_arr = numpy.zeros((len(image), len(image[0])))
    for i in range(2):
        for line in image[:]:
            image_copy += line

    index = len(image[0])
    print index
    for i in range(index, 2 * index):
        for j in range(index):
            temp = image_copy[i][j - size:j + 1 + size]
            print temp
            re_median_arr[i][j - index] = sorted(temp)[len(temp) / 2]

    return re_median_arr
