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
    color_image = cv2.imread("source/squares.png", 0)
    #  a = [[1,2,3,4,5], [6,7,8,9,10], [11,12,13,14,15], [11,12,13,14,15], [11,12,13,14,15]]
    cv2.imshow("before", color_image)
    color_image = remove_grid.remove_page_grid(color_image, 51)
    cv2.imshow("after", color_image)
    cv2.waitKey(0)

"""
def main(image_name="source/y2.jpg"):
    color_image = cv2.imread(image_name, 1)
    cv2.imshow("orig", color_image)
    image = cv2.imread(image_name, 0)
    ret, image = cv2.threshold(image, 60, 255, cv2.THRESH_BINARY)  # TODO: dynamic thresholding
    cv2.medianBlur(image, 9, image)
    cv2.imshow("pre_cont", image)
    cont_image, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    left_to_right = left_to_right_contours(contours)
    for i in xrange(len(left_to_right)): # draw numbers for ordered contours
        cv2.putText(color_image, str(i), leftmost_point(left_to_right[i]), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 5)
    cv2.drawContours(color_image, contours, -1, (255, 0, 255), 3)
    # main_contour = contours[2]
    # leftmost = tuple(main_contour[main_contour[:, :, 0].argmin()][0])
    # print leftmost
    # rect = cv2.minAreaRect(main_contour)
    # print rect
    # int_rect = [[int(num) for num in x] for x in rect if type(x) is type(tuple)]
    # print int_rect
    # cv2.rectangle(color_image, rect[0], rect[1], (0, 255, 0))
    # print rect
    # cv2.convexHull(main_contour)
    # print len(contours)
    cv2.imshow("conts", color_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
"""

if __name__ == "__main__":
    main()
