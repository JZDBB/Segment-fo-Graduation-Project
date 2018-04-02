from PIL import Image
from pylab import *
import cv2
import os
import numpy as np

path = './data/segmentData/'
filenames = os.listdir(path=path)
for filename in filenames:
    rects = []
    pic_path = os.path.join(path, filename)
    img = array(Image.open(pic_path))
    if img.shape[1] < 2500:
        ratio0 = img.shape[1] / 2500.0
        img = cv2.resize(img, (2500, int(2500 * img.shape[0] / img.shape[1])))
    imshow(img)
    print('Please click 4 points')
    x = ginput(4)
    print('you clicked:', x)
    show()
    while x[2][0]> 50 and x[2][1]> 50:
        rect = array([list(x[0]),list(x[1]),list(x[2]),list(x[3])])
        rects.append(np.int32(rect))
        imshow(img)
        print('Please click 4 points')
        x = ginput(4)
        print('you clicked:', x)
        show()

    # rects.append(np.int32(array([list(x[0]),list(x[1]),list(x[2]),list(x[3])])))

    with open('./data/data.txt', 'a') as f:
        f.write(pic_path + ':')
        for rect in rects:
            # pt1, pt2, pt3, pt4 = str(rect[0][0]) + ' ' + str(rect[0][1]), str(rect[1][0]) + ' ' + str(rect[1][1]), str(
            #     rect[2][0]) + ' ' + str(rect[2][1]), str(rect[3][0]) + ' ' + str(rect[3][1])
            pt1, pt2, pt3, pt4 = str(rect[0]), str(rect[1]), str(rect[2]), str(rect[3])
            f.write(pt1 + ' ' + pt2 + ' ' + pt3 + ' ' + pt4 + ';')
        f.write('\n')
        f.close()


