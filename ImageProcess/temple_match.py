import cv2
import numpy as np

MIN_MATCH_COUNT = 4

class TempleMatch(object):
    def __init__(self):
        self.rect = []
        self.templates = []
        self.width = []
        self.height = []

    def read_template(self, template):
        self.templates.append(template)
        width, height = template.shape[::-1]
        self.width.append(width)
        self.height.append(height)

    def normal_match(self, img, method, threshold, type):
        flag = False
        for template in self.templates:
            if type:
            # recignize a picture with a sigle object
                res = cv2.matchTemplate(img, template, method)
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
                res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
                if np.max(res)<threshold:
                    flag = False
                else:
                    loc = np.where(res >= threshold)
                    for pt in zip(*loc[::-1]):
                        self.rect.append(pt)
                    flag = True

        return self.rect, flag

    def sift_match(self, img):
        flag = False
        for template in self.templates:
            # preprocess
            gray1 = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Create SIFT object
            sift = cv2.xfeatures2d.SIFT_create()
            # Create flann matcher
            matcher = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), {})  # parameters can be ajusted

            # Detect keypoints and compute keypointer descriptors
            kpts1, descs1 = sift.detectAndCompute(gray1, None)
            kpts2, descs2 = sift.detectAndCompute(gray2, None)

            # knnMatch to get Top2
            matches = matcher.knnMatch(descs1, descs2, 2)
            # Sort by their distance.
            matches = sorted(matches, key=lambda x: x[0].distance)

            # Ratio test, to get good matches.
            good = [m1 for (m1, m2) in matches if m1.distance < 0.7 * m2.distance]

            canvas = img.copy()

            # find homography matrix
            # 当有足够的健壮匹配点对（至少4个）时
            if len(good) > MIN_MATCH_COUNT:
                flag = True
                # 从匹配中提取出对应点对
                # (queryIndex for the small object, trainIndex for the scene )
                src_pts = np.float32([kpts1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dst_pts = np.float32([kpts2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
                # find homography matrix in cv2.RANSAC using good match points
                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                # 掩模，用作绘制计算单应性矩阵时用到的点对
                # matchesMask2 = mask.ravel().tolist()
                # 计算图1的畸变，也就是在图2中的对应的位置。
                h, w = img.shape[:2]
                pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, M)
                # 绘制边框
                cv2.polylines(canvas, [np.int32(dst)], True, (0, 255, 0), 3, cv2.LINE_AA)

                self.rect.append(np.int32(dst))
            else:
                print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))

        return self.rect, flag


    def draw_rect(self, img, rect, Color, pixel):
        for rectagle in rect:
            bottom_right = (rectagle[0] + self.width + pixel, rectagle[1] + self.height + pixel)
            cv2.rectangle(img, rectagle, bottom_right, Color, 2 * pixel)
        return img