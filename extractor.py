import cv2
from remove_grid import remove_page_grid
import copy
import os
import sys
import uuid
import train


def reverse(pair):
    return pair[1], pair[0]


def increase_contrast_brightness(image, alpha, beta):
    for i in xrange(len(image)):
        for j in xrange(len(image[i])):
            image[i][j] = image[i][j] * alpha + beta
    return image


class Image(object):
    @classmethod
    def from_image(cls, image):
        """copy constructor from another image"""
        a = cls(image.source)
        a.color_image = image.color_image
        a.bw_image = image.bw_image
        a.binirize_image()
        a.imshow()
        return a

    def __init__(self, source):
        self.source = source
        self.bw_image = cv2.resize(cv2.imread(source, 0),(800,600))
        self.color_image = cv2.resize(cv2.imread(source),(800,600))
        self.orignal_color_image = self.color_image
        self.bin_image = self.binirize_image()
        self.__components = None

    WINDOW_SIZE = 4

    def erase_drawing(self):
        """Resets Drawn components"""
        self.color_image = self.orignal_color_image

    def dynamic_binirize_image(self):
        self.binirize_image()
        self.draw_components()
        self.imshow()
        cv2.createTrackbar("Window Size", "Image", self.WINDOW_SIZE, 50, onChange=None)
        self.erase_drawing()

    def binirize_image(self):
        """Updates self.bin_image using existing bw_image and adaptive thresh"""
        length = max(len(self.bw_image), len(self.bw_image[0]))
        self.bin_image = cv2.adaptiveThreshold(self.bw_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                                              int(length / self.WINDOW_SIZE) + length / self.WINDOW_SIZE % 2 + 1,
                                              15)  # TODO:C is not dynamic and does matter Note- doesn't work well with whatsapp
        # self.bin_image = cv2.threshold(self.bw_image, 180, 255, cv2.THRESH_BINARY)[1]
        # print self.bin_image
        # compressed images
        cv2.medianBlur(self.bin_image, 13, self.bin_image)
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
        # Runs a BFS starting from global_image[i][j]
        neighbors = (Image.__four_way_neighbors, Image.eight_way_neighbors)
        neighbors = neighbors[connectivity]
        queue = set()
        queue.add((i, j))
        while queue:
            current_point = queue.pop()
            points.append(current_point)
            image[current_point[0]][current_point[1]] = 255
            # cv2.imshow("debug",global_image)
            for a, b in neighbors(current_point[0], current_point[1]):
                if 0 <= a < len(image) and 0 <= b < len(image[a]) and is_black(image[a][b]):
                    queue.add((a, b))
        return Component(self, points)

    def crop(self, r):
        """crops image by dimensions r. r is the bounding rectangle from selectROI"""
        self.erase_drawing()
        self.__components = None
        self.color_image = self.color_image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        self.bw_image = self.bw_image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        self.binirize_image()
        self.color_image = self.color_image

    def find_connected_components(self, connectivity=EIGHT_WAY_NEIGHBORS):
        new_image = copy.copy(self.bin_image)
        for i in xrange(len(new_image)):
            for j in xrange(len(new_image[i])):
                if is_black(new_image[i][j]):
                    yield self.connected_component_starting_from(new_image, i, j, connectivity)

    def draw_components(self):
        for component in self.components:
            component.draw_component()

    def imshow(self):
        cv2.imshow("Image", self.color_image)
        cv2.imshow("Thresh" , self.bin_image)


clf = train.Classifier()


class EquationImage(Image):
    def __init__(self, source):
        super(EquationImage, self).__init__(source)

    def equation_string(self):
        return "".join(self.string)

    def label_components(self):
        for component in self.components:
            cv2.putText(self.color_image, component.char, reverse(component.upper_left_point), cv2.FONT_HERSHEY_COMPLEX,
                        1,
                        (255, 0, 0))

    @property
    def string(self):
        return [component.char for component in self.sorted_components]

    @property
    def sorted_components(self):
        a = sorted(self.components, key=lambda x: x.upper_left_point[1])
        for index, component in enumerate(a):
            if index > 0 and (component.char == a[index - 1].char == '-' or component.char == '='):
                component.minus_to_equal(a[index - 1])
                a.pop(index - 1)
        # print a
        return a

        # for component in components:

    def correct_string(self, new_string):
        for index, new_char in enumerate(new_string):
            self.sorted_components[index].set_char(new_char)


# TODO: streamline data addition process
class ResourceImage(Image):
    def save_resources(self, name):
        # reads file names and saves components as highest num in names+1.png
        for component in self.components:
            component.save_component_as(name)


def main(source="Source/x.png", character='x'):
    image = ResourceImage(source=source)
    # increase_contrast_brightness(global_image,1.5,0)
    color_image = image.color_image
    components = image.components

    cv2.imshow("result", color_image)  # only if you want it to draw
    print "Press S to save, any other char to quit"
    if cv2.waitKey(0) & 0xFF == ord('s'):  # saves if you press S
        print('Saved!')
        image.save_resources(components, character)

    # cv2.waitKey(0)
    cv2.destroyAllWindows()


class Component:
    def __init__(self, parent_image, points):
        self.points = points
        self.__char = "unknown"
        self.parent_image = parent_image
        self.upper_left_point = min(self.points, key=lambda x: x[0])[0], min(self.points, key=lambda x: x[1])[1]
        self.lower_right_point = max(self.points, key=lambda x: x[0])[0], max(self.points, key=lambda x: x[1])[1]

    def add_point(self, point):
        self.points.append(point)

    def image(self):
        up = self.upper_left_point
        low = self.lower_right_point
        crop = self.parent_image.bin_image[up[0]:low[0], up[1]:low[1]]
        return crop

    def __str__(self):
        return str(self.points)

    def __repr__(self):
        return str(self.upper_left_point) + "-" + str(self.lower_right_point) + self.char

    @property
    def char(self):
        if self.__char == "unknown":
            self.__char = clf.predict(self.image())
        return self.__char

    def set_char(self, val):
        self.__char = val
        self.save_component_as(val)

    def minus_to_equal(self, other_minus):
        self.__char = '='
        # self.points = self.points.extend(other_minus.points)
        # self.upper_left_point = min(self.points, key=lambda x: x[0])[0], min(self.points, key=lambda x: x[1])[1]
        # self.lower_right_point = max(self.points, key=lambda x: x[0])[0], max(self.points, key=lambda x: x[1])[1]

    def save_component_as(self, char):
        location = "Resources/" + char + "/"
        i = 0
        if not os.path.exists(location):
            os.mkdir(location)
        while os.path.exists(location + char + "_" + str(i) + ".png"):
            i += 1
        cv2.imwrite(location + char + '_' + str(i) + ".png", self.image())

    def draw_component(self):
        """Draws component and frame of component on the parent color_image"""
        # for point in component.reversed_points():
        #     cv2.rectangle(global_image, point, point, (255, 0, 0))
        cv2.rectangle(self.parent_image.color_image, reverse(self.upper_left_point),
                      reverse(self.lower_right_point), (255, 0, 0))


def is_black(point):
    return not point


FOUR_WAY_NEIGHBORS = 0
EIGHT_WAY_NEIGHBORS = 1


def four_way_neighbors(i, j):
    return (i, j - 1), (i, j + 1), (i + 1, j), (i - 1, j)


def eight_way_neighbors(i, j):
    return (i, j - 1), (i, j + 1), (i + 1, j), (i - 1, j), (i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (
        i + 1, j + 1)


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
