import cv2
import numpy as np

class TempleMatch(object):
    def __init__(self):
        self.rect = []
        self.template = []
        self.width = []
        self.height = []

    def read_template(self, template):
        self.template.append(template)
        width, height = template.shape[::-1]
        self.width.append(width)
        self.height.append(height)

    def normal_match(self, img, method, threshold, type):
        if type:
        # recignize a picture with a sigle object
            res = cv2.matchTemplate(img, self.template, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            print(min_loc, min_val, max_loc, max_val)
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            self.rect.append(top_left)
            flag = True

        else:
            res = cv2.matchTemplate(img, self.template, cv2.TM_CCOEFF_NORMED)
            if np.max(res)<threshold:
                flag = False
            else:
                loc = np.where(res >= threshold)
                for pt in zip(*loc[::-1]):
                    self.rect.append(pt)
                flag = True

        return self.rect, flag

    def sift_match(self):
        pass


    def draw_rect(self, img, rect, Color, pixel):
        for rectagle in rect:
            bottom_right = (rectagle[0] + self.width + pixel, rectagle[1] + self.height + pixel)
            cv2.rectangle(img, rectagle, bottom_right, Color, 2 * pixel)
        return img