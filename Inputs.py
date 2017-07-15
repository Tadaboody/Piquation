import cv2
import extractor


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
        gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        gray_image = extractor.pre_process(gray_image)
        # cv2.imshow("thresh", gray_image)
        components = extractor.find_connected_components(gray_image, connectivity=extractor.EIGHT_WAY_NEIGHBORS)
        for component in components:
            extractor.draw_component(color_image, component)
        cv2.imshow("after", color_image)
        # extractor.main(pic_name)
        # cv2.imwrite(pic_name, gray_image)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite("Output/webcam.png",gray_image)
            print "Saved!"
            break
            # def main():
#     take_pic("test.jpg")


if __name__ == "__main__":
    take_pic("Source/test.jpg")
