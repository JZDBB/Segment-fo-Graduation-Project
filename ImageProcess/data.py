import os
import cv2
import numpy as np

class Data(object):

    def read_images(self, path, mode):
        images = []
        filenames = os.listdir(path=path)
        for filename in filenames:
            pic_path = os.path.join(path, filename)
            images.append(cv2.imread(pic_path, mode))
        return images

    def write_images(self, path, imgs, rectangles, height, width):
        count = 1
        str = "1.png"
        for img in imgs:
            for rect in rectangles:
                pts = np.float32([[0, 0], [0, height - 1], [width - 1, height - 1], [width - 1, 0]]).reshape(-1, 1, 2)
                perspectiveM = cv2.getPerspectiveTransform(rect, pts)
                found = cv2.warpPerspective(img, perspectiveM, (width, height))
                cv2.imwrite(os.path.join(path, str.replace("1", "%d" % count)), found)
                count = count + 1


