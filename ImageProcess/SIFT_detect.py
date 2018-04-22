import cv2
MIN_MATCH_COUNT = 4


def sift_detect(img):

    sift = cv2.xfeatures2d.SIFT_create()
    kpts1, descs1 = sift.detectAndCompute(img,None)

    return len(kpts1)