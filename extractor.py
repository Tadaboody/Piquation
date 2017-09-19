import cv2
from remove_grid import remove_page_grid
import copy
import os
import sys
import uuid


def reverse(pair):
    return pair[1], pair[0]


def increase_contrast_brightness(image, alpha, beta):
    for i in xrange(len(image)):
        for j in xrange(len(image[i])):
            image[i][j] = image[i][j] * alpha + beta
    return image


class Image:
    def __init__(self, source=None, color_image=None):
        if color_image is not None:
            self.color_image = color_image
            self.bw_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        else:
            print source
            self.bw_image = cv2.imread(source, 0)
            self.color_image = cv2.imread(source)

        self.bin_image = self.binirize_image()
        self.__components = None

    def binirize_image(self):
        length = max(len(self.bw_image), len(self.bw_image[0]))
        self.bin_image = cv2.adaptiveThreshold(self.bw_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                                               int(length / 15) + length / 15 % 2 + 1,
                                               15)  # TODO:C is not dynamic and does matter Note- doesn't work well with whatsapp
        # compressed images
        cv2.medianBlur(self.bin_image, 9, self.bin_image)
        cv2.imwrite("Output/threshed.png", self.bin_image)
        return self.bin_image

    @property
    def components(self):
        if self.__components is None:
            self.__components = list(self.find_connected_components())
        return self.__components

    # These methods used to be out of class, didn't change them since
    FOUR_WAY_NEIGHBORS = 0
    EIGHT_WAY_NEIGHBORS = 1

    @staticmethod
    def __four_way_neighbors(i, j):
        return (i, j - 1), (i, j + 1), (i + 1, j), (i - 1, j)

    @staticmethod
    def eight_way_neighbors(i, j):
        # return tuple(list(__four_way_neighbors(i, j)).extend(
        #     ((i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (i + 1, j + 1))))  # Not sure why I insist on tuples
        return (i, j - 1), (i, j + 1), (i + 1, j), (i - 1, j), (i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (
            i + 1, j + 1)

    def connected_component_starting_from(self, image, i, j, connectivity=EIGHT_WAY_NEIGHBORS):
        points = list()
        # Runs a BFS starting from image[i][j]
        neighbors = (Image.__four_way_neighbors, Image.eight_way_neighbors)
        neighbors = neighbors[connectivity]
        queue = set()
        queue.add((i, j))
        while queue:
            current_point = queue.pop()
            points.append(current_point)
            image[current_point[0]][current_point[1]] = 255
            # cv2.imshow("debug",image)
            for a, b in neighbors(current_point[0], current_point[1]):
                if 0 <= a < len(image) and 0 <= b < len(image[a]) and is_black(image[a][b]):
                    queue.add((a, b))
        return Component(self, points)

    def crop(self, upper_left, down_right):
        self.__components = None
        self.color_image = self.color_image[upper_left[1]:down_right[1], upper_left[0], down_right[0]]

    def find_connected_components(self, connectivity=EIGHT_WAY_NEIGHBORS):
        new_image = copy.copy(self.bin_image)
        for i in xrange(len(new_image)):
            for j in xrange(len(new_image[i])):
                if is_black(new_image[i][j]):
                    yield self.connected_component_starting_from(new_image, i, j, connectivity)


# TODO: streamline data addition process

def binirize_image(image):
    length = max(len(image), len(image[0]))
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                                  int(length / 15) + length / 15 % 2 + 1,
                                  15)  # TODO:C is not dynamic and does matter Note- doesn't work well with whatsapp
    # compressed images
    cv2.medianBlur(image, 9, image)
    cv2.imwrite("Output/threshed.png", image)
    return image


def save_resource(image, components, name):
    # reads file names and saves components as highest num in names+1.png
    location = "Resources/" + name + "/"
    for component in components:
        i = 0
        while os.path.exists(location + name + "_" + str(i) + ".png"):
            i += 1
        cv2.imwrite(location + name + '_' + str(i) + ".png", crop_to_component(image, component))


def main(source="Source/x.png", character='x'):
    image = Image(source=source)
    # increase_contrast_brightness(image,1.5,0)
    color_image = image.color_image
    components = image.components
    for component in components:
        component.draw_component()
    cv2.imshow("result", color_image)  # only if you want it to draw
    print "Press S to save, any other char to quit"
    if cv2.waitKey(0) & 0xFF == ord('s'):  # saves if you press S
        print('Saved!')
        save_resource(image, components, character)

    # cv2.waitKey(0)
    cv2.destroyAllWindows()


class Component:
    def __init__(self, parent_image, points):
        self.points = points
        self.char = "unknown"
        self.parent_image = parent_image
        self.upper_left_point = min(self.points, key=lambda x: x[0])[0], min(self.points, key=lambda x: x[1])[1]
        self.lower_right_point = max(self.points, key=lambda x: x[0])[0], max(self.points, key=lambda x: x[1])[1]

    def add_point(self, point):
        self.points.append(point)

    def reversed_points(self):
        return (reverse(point) for point in self.points)

    def image(self):
        up = self.upper_left_point
        low = self.lower_right_point
        crop = self.parent_image.bin_image[up[0]:low[0], up[1]:low[1]]
        return crop

    def __str__(self):
        return str(self.points)

    def __repr__(self):
        return str(self.upper_left_point) + "-" + str(self.lower_right_point)

    def draw_component(component):
        """Draws component and frame of component on the image"""
        # for point in component.reversed_points():
        #     cv2.rectangle(image, point, point, (255, 0, 0))
        cv2.rectangle(component.parent_image.color_image, reverse(component.upper_left_point),
                      reverse(component.lower_right_point), (255, 0, 0))


def is_black(point):
    return not point


FOUR_WAY_NEIGHBORS = 0
EIGHT_WAY_NEIGHBORS = 1


def four_way_neighbors(i, j):
    return (i, j - 1), (i, j + 1), (i + 1, j), (i - 1, j)


def eight_way_neighbors(i, j):
    # return tuple(list(four_way_neighbors(i, j)).extend(
    #     ((i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (i + 1, j + 1))))  # Not sure why I insist on tuples
    return (i, j - 1), (i, j + 1), (i + 1, j), (i - 1, j), (i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (
        i + 1, j + 1)


# def connected_component_starting_from(image, i, j, connectivity=EIGHT_WAY_NEIGHBORS):
#     return_value = Component(image)
#     # Runs a BFS starting from image[i][j]
#     neighbors = (__four_way_neighbors, eight_way_neighbors)
#     neighbors = neighbors[connectivity]
#     queue = set()
#     queue.add((i, j))
#     while queue:
#         current_point = queue.pop()
#         return_value.add_point(current_point)
#         image[current_point[0]][current_point[1]] = 255
#         # cv2.imshow("debug",image)
#         for a, b in neighbors(current_point[0], current_point[1]):
#             if 0 <= a < len(image) and 0 <= b < len(image[a]) and is_black(image[a][b]):
#                 queue.add((a, b))
#     return return_value
#
#
# def find_connected_components(image, connectivity=EIGHT_WAY_NEIGHBORS):
#     new_image = copy.copy(image.bin_image)
#     for i in xrange(len(new_image)):
#         for j in xrange(len(new_image[i])):
#             if is_black(new_image[i][j]):
#                 yield connected_component_starting_from(new_image, i, j, connectivity)
#
#
def crop_to_component(image, component):
    up = component.upper_left_point
    low = component.lower_right_point
    crop = image.bin_image[up[0]:low[0], up[1]:low[1]]
    return crop


if __name__ == "__main__":
    if len(sys.argv) is 3:  # first argument is always the file name
        main(sys.argv[1], sys.argv[2])
    else:
        main()
