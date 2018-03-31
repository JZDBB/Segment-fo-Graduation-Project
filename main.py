from ImageProcess import temple_match, data, nms
import matplotlib.pyplot as plt
import cv2
import numpy as np
from numpy import *
import os

class SegMain(object):
    # init
    def __init__(self):
        self.data = data.Data()
        self.match = temple_match.TempleMatch()
        self.rects = []

    def Segment(self, template_path, segdata_path, result_path):
        count = 1
        # read the template picture
        # templates = self.data.read_images(template_path, None)
        # read the picture which need segment
        segdatas = self.data.read_images(segdata_path, None)
        # judge its rotate and scale (no need)
        count = 0
        for segdata in segdatas:
            count = count + 1

            # ajust its size to a Regulated template
            ratio0 = 1.0
            img = segdata
            if segdata.shape[1] < 2500:
                ratio0 = segdata.shape[1] / 2500.0
                img = cv2.resize(segdata, (2500, int(2500 * segdata.shape[0] / segdata.shape[1])))

            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            canvas = img.copy()

            # use the normal template match to recognise its frame   \
            #                                                         >  this need further consider
            # use the SIFT template match to recognise its frame     |

            # normal template match
            self.match.read_templates(template_path, None, True)
            rect, score, flag = self.match.normal_match(img_gray, 0, 0.476, False)
            pick_rect, pick_score = nms.non_max_suppression(rect, score, 0.5)
            print(pick_rect, pick_score)
            for rect_found in pick_rect:
                fillrect = np.array([[[rect_found[0], rect_found[1]],
                                      [rect_found[2], rect_found[1]],
                                      [rect_found[2], rect_found[3]],
                                      [rect_found[0], rect_found[3]]]], dtype = np.int32)
                cv2.fillPoly(img_gray, fillrect, 255)
                self.rects.append(array([[[rect_found[0], rect_found[1]],
                                          [rect_found[2], rect_found[1]],
                                          [rect_found[2], rect_found[3]],
                                          [rect_found[0], rect_found[3]]]]))
            # plt.imshow(img_gray, cmap='gray')
            # plt.show()
            print("ok")

            # SIFT template match
            self.match.read_templates(template_path, None, False)
            rect_SIFT, flag = self.match.sift_match(img_gray)
            print(rect_SIFT)
            for rect_found in rect_SIFT:
                self.rects.append(array([[rect_found[0][0],
                                          rect_found[1][0],
                                          rect_found[2][0],
                                          rect_found[3][0]]]))

            for rect_draw in self.rects:
                cv2.polylines(canvas, rect_draw, True, (0, 255, 0), 3, cv2.LINE_AA)

            plt.imshow(canvas)
            plt.show()

            filename =  result_path + str(count) + '.jpg'
            cv2.imwrite(filename, canvas)

            self.rects = []

            # save the segment picture data
            # res_path = os.path.join(result_path, 'result.txt')
            # with open(res_path, 'w') as f:
            #     for rect in self.rects:
            #         f.write(str(rect) + '\n')
            #     f.close()

            # test the accuracy (IoU)





if __name__ == '__main__':
    path = "./data"
    template = "./data/template"
    segmentData = "./data/segmentData"
    result = "./data/result/"
    obj_seg = SegMain()
    obj_seg.Segment(template, segmentData, result)