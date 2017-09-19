import cv2
import train
import extractor
import sys
from extractor import Image

def draw_and_number_components(image, components, text):
    for i, component in enumerate(components):
        # extractor.draw_component(image, component)
        char = text[i]
        cv2.putText(image, text[i], extractor.reverse(component.upper_left_point), cv2.FONT_HERSHEY_COMPLEX, 1,
                    (255, 0, 0))


clf = train.Classifier()


def extract_and_solve(image):
    pass


def predict_and_print_image(image):
    components = image.components
    print components
    predictions = clf.predict(components)
    draw_and_number_components(image.color_image, components, predictions)
    cv2.imshow("im", image.color_image)


def main(image_name="source/y2.jpg"):
    image = Image(image_name)
    components = image.components
    predictions = clf.predict(components)
    print predictions
    draw_and_number_components(image.color_image, components, predictions)
    cv2.imshow("im", image.color_image)
    cv2.waitKey(0)


if __name__ == '__main__':
    if len(sys.argv) is 2:  # first argument is always the file name
        main(sys.argv[1])
    else:
        main()
