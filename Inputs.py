import cv2
import extractor
from test import predict_and_print_image
from extractor import Image

class NoCameraException(Exception):
    def __str__(self):
        return "User has valid camera connected"


def take_pic(pic_name):
    cap = cv2.VideoCapture(0)
    if not cap:
        raise NoCameraException()
    while cap:
        ret, color_image = cap.read()
        # cv2.imshow("hey", color_image)
        image = Image(color_image=color_image)
        # try:
        predict_and_print_image(image)
        if cv2.waitKey(1) & 0xFF == ord('p'):
            cv2.waitKey(0)
        # except:
        #     cv2.imshow("im",color_image)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite("Output/webcam.png",image.bw_image)
            print "Saved!"
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            # def main():
#     take_pic("test.jpg")


if __name__ == "__main__":
    take_pic("Source/test.jpg")
