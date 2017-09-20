import cv2
import train
import extractor
import sys
from extractor import EquationImage


clf = train.Classifier()


def extract_and_solve(image):
    pass


def main(image_name="source/y2.jpg"):
    image = EquationImage(image_name)
    # components = global_image.components
    # predictions = clf.predict(components)
    print image.equation_string()
    # label_components(global_image.color_image, components, predictions)
    image.label_components()
    image.draw_components()
    image.imshow()
    cv2.waitKey(0)


if __name__ == '__main__':
    if len(sys.argv) is 2:  # first argument is always the file name
        main(sys.argv[1])
    else:
        main()
