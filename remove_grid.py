import numpy
import cv2


def remove_page_grid(image, median_size):  # numpy.median is a function
    cv2.imshow("before", image)
    return_image = horizontal_median_filter(image, median_size)
    cv2.imshow("after 1", return_image)
    return_image = vertical_median_filter(return_image, median_size)
    cv2.imshow("after 2", return_image)
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

    index = len(image[0])
    for i in range(len(image)):
        for j in range(index, 2*index):
            temp = image_copy[i][j - size:j + 1 + size]
            re_median_arr[i][j - index - 1] = sorted(list(temp))[len(temp) / 2]
    return re_median_arr


def vertical_median_filter(image, size):
    size = (size - 1) / 2
    image_copy = list(numpy.zeros(3 * (len(image), len(image[0])), numpy.uint8))

    for i, line in enumerate(image_copy[:]):
        image_copy[i] = list(line)

    re_median_arr = numpy.zeros((len(image), len(image[0])), numpy.uint8)

    for i in range(len(image_copy)):
        for j in range(len(image_copy[i])):
            image_copy[i][j] = image[i % len(image)][j]

    index = len(image)
    for i in range(index, 2 * index):
        for j in range(len(image_copy[i])):
            #  temp = image_copy[i][j - size:j + 1 + size]
            temp = [element[0] for element in image_copy[i - size:i + size + 1]]
            re_median_arr[i - index - 1][j] = sorted(list(temp))[len(temp) / 2]
    return re_median_arr

