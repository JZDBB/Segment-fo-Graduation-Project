import os
import cv2

class Data(object):

    def read_images(self, path, mode):
        images = []
        filenames = os.listdir(path=path)
        for filename in filenames:
            pic_path = os.path.join(path, filename)
            images.append(cv2.imread(pic_path, mode))
        return images

    def write_images(self):
        pass

