import cv2


class NoCameraException(Exception):
    def __str__(self):
        return "User has valid camera connected"


def take_pic():
    cap = cv2.VideoCapture(0)
    if not cap:
        raise NoCameraException()
    while cap:
        ret, image = cap.read()
        cv2.imshow("Camera",image)
        if cv2.waitKey(1) & 0xFF == ord(' '):
            cv2.imwrite("Source/webcam.png", image)

            return image


# take_pic("test.jpg")


if __name__ == "__main__":
    take_pic()
