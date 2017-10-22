import cv2
import remove_grid


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


def main():
    color_image = cv2.imread("Source/squares.png", 0)
    #  a = [[1,2,3,4,5], [6,7,8,9,10], [11,12,13,14,15], [11,12,13,14,15], [11,12,13,14,15]]
    cv2.imshow("before", color_image)
    color_image = remove_grid.remove_page_grid(color_image, 51)
    cv2.imshow("after", color_image)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()
