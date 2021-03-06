from sklearn.svm import LinearSVC
import os
import cv2

SIZE = (30, 30)


def char_not_empty(char):
    return bool(os.listdir("Resources/" + char))


def normalize(image):
    for i in xrange(len(image)):
        for j in xrange(len(image[i])):
            if image[i][j]:
                image[i][j] = 1
    return image


def load_data_from_resources(character):
    location = "Resources/" + character
    return [cv2.imread(location + "/" + filename, 0) for filename in
            os.listdir(location)], [character for i in
                                    os.listdir(location)]


# x_classifier = LinearSVC()

class Classifier(LinearSVC):
    def __init__(self):
        super(Classifier, self).__init__()
        datasets = [load_data_from_resources(character) for character in next(os.walk("Resources"))[1] if
                    char_not_empty(character)]
        data = []
        target = []
        for datas, targets in datasets:
            data.extend(datas)
            target.extend(targets)
        # shape = [global_image.shape for global_image in data]
        data = [self.pre_proccess(image) for image in data]
        # data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.30 ) #for testing
        self.fit(data, target)

    @staticmethod
    def pre_proccess(image):
        try:
            a = cv2.resize(image, SIZE).flatten()
        except:
            a = image.flatten()
        return a

    def predict(self, image):
        a = "N/A"
        try:
            a= super(Classifier, self).predict([self.pre_proccess(image)])[0]
        except:
            pass
        print a
        return a
