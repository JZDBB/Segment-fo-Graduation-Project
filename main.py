from ImageProcess import temple_match, data, nms
import matplotlib.pyplot as plt
import cv2
import numpy as np

class SegMain(object):
    # init
    def __init__(self):
        self.data = data.Data()
        self.match = temple_match.TempleMatch()

    def Segment(self, template_path, segdata_path, result_path):
        count = 1
        # read the template picture
        templates = self.data.read_images(template_path, None)
        # read the picture which need segment
        segdatas = self.data.read_images(segdata_path, None)
        # judge its rotate and scale (no need)

        for segdata in segdatas:
            # ajust its size to a Regulated template
            ratio0 = 1.0
            if segdata.shape[1] < 2500:
                ratio0 = segdata.shape[1] / 2500.0
                img = cv2.resize(segdata, (2500, int(2500 * segdata.shape[0] / segdata.shape[1])))

            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # use the normal template match to recognise its frame   \
            #                                                         >  this need further consider
            # use the SIFT template match to recognise its frame     |

            # normal template match
            self.match.read_templates(templates)
            rect, score, flag = self.match.normal_match(img_gray, 0, 0.35, False)
            pick_rect, pick_score = nms.non_max_suppression(rect, score, 0.5)
            print(pick_rect, pick_score)
            for rect_found in pick_rect:
                fillrect = np.array([[[rect_found[0],rect_found[1]], [rect_found[2],rect_found[1]], [rect_found[2],rect_found[3]], [rect_found[0],rect_found[3]]]], dtype = np.int32)
                cv2.fillPoly(img_gray, fillrect, 255)
            # img_rect = self.match.draw_rect(img_gray, pick_rect, 0, 5)
            plt.imshow(img_gray, cmap='gray')
            plt.show()

            # SIFT template match
            # self.match.read_templates(templates)
            # rect, flag = self.match.sift_match(img_gray)
            # print(rect)
            # img_rect = self.match.draw_rect(img_gray, rect, 0, 5)
            # plt.imshow(img_rect, cmap='gray')
            # plt.show()

            # save the segment picture



if __name__ == '__main__':
    path = "./data"
    template = "./data/template"
    segmentData = "./data/segmentData"
    result = "./data/result/"
    obj_seg = SegMain()
    obj_seg.Segment(template, segmentData, result)