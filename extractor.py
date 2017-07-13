import cv2
from remove_grid import remove_page_grid
import copy


def leftmost_point(contour):
    return tuple(contour[contour[:, :, 0].argmin()][0])


def left_to_right_contours(contours):
    """given a list of contours returns a list of the same contours sorted by leftmost """
    # leftmost_array = [(leftmost_point(cont),contours.index(cont)) for cont in
    #                   contours]  # returns a list of the leftmost point of every contour (x,y)
    leftmost_array = [(index, leftmost_point(contour)) for index, contour in enumerate(contours)]
    # for i in xrange(len(contours)):
    #     leftmost_array.append((leftmost_point(contours[i]), i))
    leftmost_array.sort(key=lambda x: x[1])
    print leftmost_array
    sorted_contours = [contours[index] for index, data in
                       leftmost_array]  # list of contours sorted in the order of leftmost points left to right
    return sorted_contours


def reverse(pair):
    return pair[1], pair[0]


def increase_contrast_brightness(image, alpha, beta):
    for i in xrange(len(image)):
        for j in xrange(len(image[i])):
            image[i][j] = image[i][j] * alpha + beta


def draw_component(image, component):
    """Draws frame of component on the image"""
    for point in component.points:
        point = reverse(point)
        cv2.rectangle(image, point, point, (255, 0, 0))
    cv2.rectangle(image, reverse(component.upper_left_point()), reverse(component.lower_right_point()), (255, 0, 0))


def crop_to_component(image, component):
    up = component.upper_left_point()
    low = component.lower_right_point()
    crop = image[up[0]:low[0], up[1]:low[1]]
    return crop


def contour_stuff(threshed_image, drawable_image):
    cont_image, contours, hierarchy = cv2.findContours(threshed_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    left_to_right = left_to_right_contours(contours)
    for i in xrange(len(left_to_right)):  # draw numbers for ordered contours
        cv2.putText(drawable_image, str(i), leftmost_point(left_to_right[i]), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255),
                    5)
    cv2.drawContours(drawable_image, contours, -1, (255, 0, 255), 3)


# TODO: streamline data addition process

def main(image_name="resources/3.jpg"):
    color_image = cv2.imread(image_name, 1)
    cv2.imshow("orig", color_image)
    image = cv2.imread(image_name, 0)
    # increase_contrast_brightness(image,1.5,0)
    length = max(len(image), len(image[0]))
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                                  int(length / 15) + length / 15 % 2 - 1,
                                  15)  # TODO:maybe less of a bodge Note- doesn't work well with whatsapp compressed
    # images
    cv2.medianBlur(image, 9, image)
    cv2.imshow("threshed", image)
    cv2.imwrite("Output/threshed.png", image)
    components = find_connected_components(image, EIGHT_WAY_NEIGHBORS)

    for index, component in enumerate(components):
        cv2.imwrite("Resources/3/" + str(index) + ".png", crop_to_component(image, component))
        draw_component(color_image, component)
    cv2.imwrite("Output/output.png", color_image)
    cv2.imshow("conts", color_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


class Component:
    def __init__(self):
        self.points = list()

    def add_point(self, point):
        self.points.append(point)

    def upper_left_point(self):
        return min(self.points, key=lambda x: x[0])[0], min(self.points, key=lambda x: x[1])[1]

    def lower_right_point(self):
        return max(self.points, key=lambda x: x[0])[0], max(self.points, key=lambda x: x[1])[1]

    def __str__(self):
        return str(self.points)

    def __repr__(self):
        return str(self.upper_left_point()) + "-" + str(self.lower_right_point())


FOUR_WAY_NEIGHBORS = 0
EIGHT_WAY_NEIGHBORS = 1


def four_way_neighbors(i, j):
    return (i, j - 1), (i, j + 1), (i + 1, j), (i - 1, j)


def eight_way_neighbors(i, j):
    # return tuple(list(four_way_neighbors(i, j)).extend(
    #     ((i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (i + 1, j + 1))))  # Not sure why I insist on tuples
    return (i, j - 1), (i, j + 1), (i + 1, j), (i - 1, j), (i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (
        i + 1, j + 1)


def is_black(point):
    return not point


def connected_component_starting_from(image, i, j, connectivity=FOUR_WAY_NEIGHBORS):
    return_value = Component()
    # Runs a BFS starting from image[i][j]
    neighbors = (four_way_neighbors, eight_way_neighbors)
    neighbors = neighbors[connectivity]
    queue = set()
    queue.add((i, j))
    while queue:
        current_point = queue.pop()
        return_value.add_point(current_point)
        image[current_point[0]][current_point[1]] = 255
        # cv2.imshow("debug",image)
        for a, b in neighbors(current_point[0], current_point[1]):
            if 0 <= a < len(image) and 0 <= b < len(image[a]) and is_black(image[a][b]):
                queue.add((a, b))
    return return_value


def find_connected_components(image, connectivity=FOUR_WAY_NEIGHBORS):
    new_image = copy.copy(image)
    for i in xrange(len(new_image)):
        for j in xrange(len(new_image[i])):
            if is_black(new_image[i][j]):
                yield connected_component_starting_from(new_image, i, j, connectivity)


if __name__ == "__main__":
    main()
