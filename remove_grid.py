import numpy
import cv2


def remove_page_grid(image):  # numpy.median is a function
    median_size = 7
    return_image = vertical_median_filter(image, median_size)
    return_image = horizontal_median_filter(return_image, median_size)
    return return_image


def horizontal_median_filter(image, size):
    size = (size - 1) / 2
    image_copy = list(numpy.zeros((len(image), 3*len(image[0])), numpy.int16))

    for i, line in enumerate(image_copy[:]):
        image_copy[i] = list(line)

    re_median_arr = numpy.zeros((len(image), len(image[0])), numpy.int16)

    for i in range(len(image_copy)):
        for j in range(len(image_copy[i])):
            image_copy[i][j] = image[i][j % len(image[i])]

    index = len(image[0])
    for i in range(len(image)):
        for j in range(index, 2*index):
            temp = image_copy[i][j - size:j + 1 + size]
            re_median_arr[i][j - index - 1] = sorted(list(temp))[len(temp) / 2]

    return re_median_arr


def vertical_median_filter(image, size):
    pass
