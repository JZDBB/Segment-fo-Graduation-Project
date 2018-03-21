import os
import cv2

class ReadData(object):

    def read_images(self, path, mode):
        images = []
        filenames = os.listdir(path=path)
        for filename in filenames:
            pic_path = os.path.join(path, filename)
            images.append(cv2.imread(pic_path, mode))
        return images

    def read_files(self):
        pass

