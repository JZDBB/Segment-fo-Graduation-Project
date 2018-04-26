from ImageProcess import temple_match, data, nms, IoU, get_angle
import matplotlib.pyplot as plt
import cv2
import numpy as np
from numpy import *
import os
import time

class SegMain(object):
    # init
    def __init__(self):
        self.data = data.Data()
        self.match = temple_match.TempleMatch()
        self.rects = []

    def Segment(self, template_path, segdata_path, result_path):

        total_time = []
        count = 1
        # read the template picture
        # templates = self.data.read_images(template_path, None)
        # read the picture which need segment
        # segdatas = self.data.read_images(segdata_path, None)
        # judge its rotate and scale (no need)
        # count = 0
        # for segdata in segdatas:
        #     count = count + 1
        accuracy = []
        with open('./data/data.txt', 'r') as f:
            data = f.readlines()  # txt中所有字符串读入data
            for line in data:
                print(line)
                mesg = line.split(':')  # 将单个数据分隔开存好
                pic_path = mesg[0]
                mesgs = mesg[1].split(';')
                test_rects = []
                # print(len(mesgs))
                for i in range(len(mesgs)-1):
                    m = mesgs[i].split(' ')
                    test_rects.append(array([[[int(m[0]), int(m[1])], [int(m[2]), int(m[3])], [int(m[4]), int(m[5])], [int(m[6]), int(m[7])]]]))
                segdata = cv2.imread(pic_path)
                # ajust its size to a Regulated template
                ratio0 = 1.0

                time_start = time.time()

                img = segdata
                if segdata.shape[1] < 2500:
                    ratio0 = segdata.shape[1] / 2500.0
                    img = cv2.resize(segdata, (2500, int(2500 * segdata.shape[0] / segdata.shape[1])))

                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                canvas = img.copy()
                self.rects = []
                # use the normal template match to recognise its frame   \
                #                                                         >  this need further consider
                # use the SIFT template match to recognise its frame     |

                # normal template match
                self.match.read_templates(template_path, None, True)
                rect, score, flag = self.match.normal_match(img_gray, 0, False)
                pick_rect, pick_score = nms.non_max_suppression(rect, score, 0.5)
                # print(pick_rect, pick_score)
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
                # print("ok")

                # SIFT template match
                self.match.read_templates(template_path, None, False)
                rect_SIFT, flag = self.match.sift_match(img_gray)
                # print(rect_SIFT)

                total_time.append(time.time() - time_start)
                for rect_found in rect_SIFT:
                    if abs(get_angle.get_cos(rect_found[0][0], rect_found[1][0], rect_found[2][0]))< float(1/5):
                        self.rects.append(array([[rect_found[0][0],
                                                  rect_found[1][0],
                                                  rect_found[2][0],
                                                  rect_found[3][0]]]))

                rects = self.rects

                for rect_draw in rects:
                    cv2.polylines(canvas, rect_draw, True, (0, 255, 0), 3, cv2.LINE_AA)

                # for rect_draw in test_rects:
                #     cv2.rectangle(canvas, rect_draw,(0,0,255),3)

                # plt.imshow(canvas)
                # plt.show()

                filename =  result_path + str(count) + '.jpg'
                cv2.imwrite(filename, canvas)
                count = count + 1
                # save the segment picture data
                # res_path = os.path.join(result_path, 'result.txt')
                # with open(res_path, 'w') as f:
                #     for rect in self.rects:
                #         f.write(str(rect) + '\n')
                #     f.close()

                # test the accuracy (IoU)
                for i in range(len(test_rects)):
                    iou = []
                    test_rect = test_rects[i]
                    for rect in self.rects:
                        # iou.append(IoU.calculateIoU((np.min(test_rect[:, :, 0]), np.min(test_rect[:, :, 1]), np.max(test_rect[:, :, 0]), np.max(test_rect[:, :, 1])), (np.min(rect[:, :, 0]), np.min(rect[:, :, 1]), np.max(rect[:, :, 0]), np.max(rect[:, :, 1]))))
                        iou.append(IoU.Polygonal_IOU(img_gray, [rect[0][0], rect[0][0][0]], [test_rect[0][0], test_rect[0][0][0]]))
                    if iou == []:
                        pass
                    else:
                        print('accuracy: ' + str(max(iou)))
                        accuracy.append(max(iou))

        print('total accuracy: ' + str(mean(accuracy)))
        print('total used time: %s s' %str(mean(total_time)))




if __name__ == '__main__':
    path = "./data"
    template = "./data/template"
    segmentData = "./data/segmentData"
    result = "./data/result/"
    obj_seg = SegMain()
    obj_seg.Segment(template, segmentData, result)