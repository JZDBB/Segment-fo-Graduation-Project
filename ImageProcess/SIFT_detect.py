import cv2
MIN_MATCH_COUNT = 4


def sift_detect(img):

    gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    kpts1, descs1 = sift.detectAndCompute(gray1,None)

    return len(kpts1)