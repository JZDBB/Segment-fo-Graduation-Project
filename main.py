from ImageProcess import temple_match, data, nms
import matplotlib.pyplot as plt
import cv2

class SegMain(object):
    # init
    def __init__(self):
        self.data = data.Data()

    def Segment(self, template_path, segdata_path, result_path):
        # read the template picture
        template = self.data.read_images(template_path, None)
        # read the picture which need segment
        segdatas = self.data.read_images(segdata_path, None)
        # judge its rotate and scale (未完成 思考中)

        for segdata in segdatas:
            # ajust its size to a Regulated template
            ratio0 = 1.0
            if segdata.shape[1] < 2500:
                ratio0 = segdata.shape[1] / 2500.0
                img = cv2.resize(segdata, (2500, int(2500 * segdata.shape[0] / segdata.shape[1])))

            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imshow('', img_gray)
            cv2.waitKey(0)

            # use the normal template match to recognise its frame   \
            #                                                         >  this need further consider
            # use the SIFT template match to recognise its frame     |


            # use its frame and picture to segment

            # save the segment picture


    pass


if __name__ == '__main__':
    path = "./data"
    template = "./data/template"
    segmentData = "./data/segmentData"
    result = "./data/result/"
    obj_seg = SegMain()
    obj_seg.Segment(template, segmentData, result)