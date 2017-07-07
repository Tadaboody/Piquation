import cv2
import exceptions
from main import main

class NoCameraException(Exception):
    def __str__(self):
        return "User has valid camera connected"


def take_pic(pic_name):
    cap = cv2.VideoCapture(0)
    if not cap:
        raise NoCameraException()
    while cap:
        ret, image = cap.read()
        cv2.imshow("hey", image)
        cv2.imwrite(pic_name, image)
        main(pic_name)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# def main():
#     take_pic("test.jpg")


if __name__ == "__main__":
    take_pic("Source/test.jpg")
    main()
