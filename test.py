import cv2
import train
import extractor
import sys


def draw_and_number_components(image, components, text):
    for i, component in enumerate(components):
        # extractor.draw_component(image, component)
        char = text[i]
        cv2.putText(image, text[i], extractor.reverse(component.upper_left_point()), cv2.FONT_HERSHEY_COMPLEX, 1,
                    (255, 0, 0))


def main(image_name="source/y2.jpg"):
    image = cv2.imread(image_name, 0)
    clr_image = cv2.imread(image_name)
    image = extractor.pre_process(image)
    components = extractor.find_connected_components(image, connectivity=extractor.EIGHT_WAY_NEIGHBORS)
    test_data = [train.pre_proccess(extractor.crop_to_component(image, component)) for component in components]
    clf = train.model()
    predictions = clf.predict(test_data)
    print predictions
    draw_and_number_components(clr_image, extractor.find_connected_components(image), predictions)
    cv2.imshow("im", clr_image)
    cv2.waitKey(0)


if __name__ == '__main__':
    if len(sys.argv) is 2:  # first argument is always the file name
        main(sys.argv[1])
    else:
        main()
