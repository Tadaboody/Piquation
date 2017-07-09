import numpy
import cv2


def remove_page_grid(image, median_size):  # numpy.median is a function
    return_image = horizontal_median_filter(image, median_size)
    return_image = vertical_median_filter(return_image, median_size)
    return return_image


def horizontal_median_filter(image, size):
    size = (size - 1) / 2
    image_copy = list(numpy.zeros((len(image), 3*len(image[0])), numpy.uint8))

    for i, line in enumerate(image_copy[:]):
        image_copy[i] = list(line)

    re_median_arr = numpy.zeros((len(image), len(image[0])), numpy.uint8)

    for i in range(len(image_copy)):
        for j in range(len(image_copy[i])):
            image_copy[i][j] = image[i][j % len(image[i])]

    last_value = 0
    index = len(image[0])
    for i in range(len(image)):
        last_value = progress_bar(i, last_value,    float(len(image)))
        for j in range(index, 2*index):
            temp = image_copy[i][j - size:j + 1 + size]
            re_median_arr[i][j - index - 1] = sorted(list(temp))[len(temp) / 2]
    return re_median_arr


def vertical_median_filter(image, size):
    size = (size - 1) / 2
    image_copy = numpy.zeros((3 * len(image), len(image[0])), numpy.uint8)

    for i, line in enumerate(image_copy[:]):
        image_copy[i] = list(line)

    re_median_arr = numpy.zeros((len(image), len(image[0])), numpy.uint8)

    for i in range(len(image_copy)):
        for j in range(len(image_copy[i])):
            image_copy[i][j] = image[i % len(image)][j]

    index = len(image)
    last_value = 0
    for i in range(index, 2 * index):
        last_value = progress_bar(i-index, last_value, float(len(image)))
        for j in range(len(image_copy[i])):
            temp = [element[j] for element in image_copy[i - size:i + size + 1]]
            re_median_arr[i - index - 1][j] = sorted(list(temp))[len(temp) / 2]
    return re_median_arr


def progress_bar(value, last_value, max_value):
    progress = float(int(1000*float(value)/max_value))/1000
    if progress != last_value:
        print 100*progress, '%'
        return progress
    return last_value
