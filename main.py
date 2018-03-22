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
        for segdata in segdatas:
            cv2.imshow('', segdata)
            cv2.waitKey(0)
            # plt.imshow(segdata, cmap='gray')
            # plt.show()
        print("over")
        # judge its rotate and scale

        # ajust its size to a Regulated template
        # for segdata in segdatas:


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