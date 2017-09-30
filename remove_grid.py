import numpy
import cv2
import time


def remove_page_grid(image, median_size):  # numpy.median is a function
    t1 = time.time()
    return_image = horizontal_median_filter(image, median_size)
    return_image = cv2.transpose(horizontal_median_filter(cv2.transpose(return_image), median_size))
    t2 = time.time()
    print "Time it took to run the function: " + str((t2 - t1))
    return return_image


def horizontal_median_filter(image, size):
    size = (size - 1) / 2

    image_copy = list(numpy.zeros((len(image), 2*size + len(image[0])), numpy.uint8))
    re_median_arr = numpy.zeros((len(image), len(image[0])), numpy.uint8)

    # left and right padding
    for i in xrange(len(image_copy)):
        for j in xrange(size):
            image_copy[i][j] = image[i][j + len(image[0]) - size]  # left side padding
            image_copy[i][j + size + len(image[0])] = image[i][j]  # right side padding

    # fill middle
    for i in xrange(len(image_copy)):
        for j in xrange(len(image[0])):
            image_copy[i][j+size] = image[i][j]

    size = 2*size + 1  # return size to original median size

    for i in xrange(len(image)):
        for j in xrange(len(image[0])):
            temp = image_copy[i][j:j + size]  # take the window in size of the original median window size
            re_median_arr[i][j] = median(temp)  # take median of median window

    return re_median_arr  # return image after


def median(array):
    return sorted(array)[len(array)/2]
