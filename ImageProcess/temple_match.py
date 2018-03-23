import cv2
import numpy as np
import os
# from matplotlib.pyplot import plt

MIN_MATCH_COUNT = 4

class TempleMatch(object):
    def __init__(self):
        self.templates = []

    def read_templates(self, path, mode):
        with open('./data/template.txt', 'r') as f:
            data = f.readlines()  # txt中所有字符串读入data
            for line in data:
                mesg = line.split(' ')  # 将单个数据分隔开存好
                pic_path = os.path.join(path, mesg[0])
                if mode == None:
                    template = cv2.imread(pic_path)

                else:
                    template = cv2.imread(pic_path, mode)
                begin = [int(mesg[1]), int(mesg[2])]
                end = [int(mesg[3]), int(mesg[4])]
                self.templates.append([template, begin, end])

        # width, height = template.shape[::-1]
        # self.width.append(width)
        # self.height.append(height)

    def normal_match(self, img, method, threshold, type):
        """
        :param img: img need be segmented
        :param method: the Similarity metrics (相似性度量准则)
        :param threshold: threshould
        :param type: one object(True) or more objects(False)
        :return: the rectangle with width and height and sucess or not
        """
        flag = False
        score = []
        rect = []
        for template_line in self.templates:

            template = cv2.cvtColor(template_line[0], cv2.COLOR_BGR2GRAY)
            begin = template_line[1]
            end = template_line[2]
            width, height = template.shape[::-1]
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
                rect.append([top_left[0], top_left[1], top_left[0] + width, top_left[1] + height])
                flag = True

            else:
                res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
                print(np.max(res))
                if np.max(res)<threshold:
                    flag = False
                else:
                    loc = np.where(res >= threshold)
                    for pt in zip(*loc[::-1]):
                        rect.append([pt[0] - begin[0], pt[1] - begin[1], pt[0] + width + end[0], pt[1] + height + end[1]])
                        score.append(res[pt[1], pt[0]])
                        print(pt)
                        print(res[pt[1], pt[0]])
                    flag = True

        return rect, score, flag

    def sift_match(self, img):
        """
        :param img: img need be segmented (image need be gray)
        :return: the rectangle with width and height and sucess or not
        """
        flag = False
        rect = []
        for template in self.templates:
            # preprocess
            gray1 = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            gray2 = img
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
            good = [m1 for (m1, m2) in matches if m1.distance < 0.6 * m2.distance]

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
                # 计算图1的畸变，也就是在图2中的对应的位置。
                h, w = template.shape[:2]
                pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, M)
                # 绘制边框
                # cv2.polylines(canvas, [np.int32(dst)], True, (0, 255, 0), 3, cv2.LINE_AA)
                perspectiveM = cv2.getPerspectiveTransform(np.float32(dst), pts)
                found = cv2.warpPerspective(img, perspectiveM, (w, h))
                dst = np.int32(dst)
                cv2.imwrite("./data/result/found.png", found)
                rect.append([dst[0][0][0], dst[0][0][1], dst[2][0][0] + w, dst[2][0][1] + h])
            else:
                print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))

        return rect, flag

    def draw_rect(self, img, rect, Color, pixel):
        for rectagle in rect:
            # bottom_right = (rectagle[0] + self.width + pixel, rectagle[1] + self.height + pixel)
            x0, y0, x1, y1 = rectagle[0:4]
            cv2.rectangle(img, (x0, y0), (x1, y1), Color, 2 * pixel)
        return img