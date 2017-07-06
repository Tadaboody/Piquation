import cv2
def main():
    image_color = cv2.imread("source/y2.jpg",1)
    cv2.imshow("orig",image_color)
    image = cv2.imread("source/y2.jpg",0)
    ret, image = cv2.threshold(image, 60, 255, cv2.THRESH_BINARY)
    cv2.medianBlur(image,7,image)
    cv2.imshow("pre_cont",image)
    cont_image, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    i=3
    print len(contours)
    cv2.drawContours(image_color, contours, 0, (255, 0, 255), 3, hierarchy=hierarchy)
    cv2.imshow("a",image_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
