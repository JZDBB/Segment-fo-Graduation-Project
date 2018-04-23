from PIL import Image
from pylab import *
import os
import cv2
import numpy as np
from ImageProcess import SIFT_detect

path_model = './data/template/model/model.jpg'
rects = []
img_r = cv2.imread(path_model)
img_tem = cv2.imread(path_model, 0)
height, width = shape(img_tem)
img = array(Image.open(path_model))
imshow(img)
print('Please click 2 points')
x = ginput(2)
print('you clicked:', x)
show()
while x[1][0] > 50 and x[1][1] > 50:
    rects.append(np.int32(x))
    imshow(img)
    print('Please click 4 points')
    x = ginput(2)
    print('you clicked:', x)
    show()

max_tem = 0
min_tem = 0
canvas = img_r.copy()
count = 0

for rect in rects:
    count = count + 1
    path = './data/template/template_model'
    names = os.listdir(path)
    cv2.rectangle(canvas, (rect[0][0], rect[0][1]), (rect[1][0], rect[1][1]), (0, 255, 0), 3)
    str_tem = 'template'+str(count)
    cv2.putText(canvas, str_tem, (rect[0][0]-1, rect[0][1]-1), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 2)
    cv2.imshow('', canvas)
    cv2.waitKey()
    template_t = img_tem[rect[0][1]:rect[1][1], rect[0][0]:rect[1][0]]
    keyPoints = SIFT_detect.sift_detect(template_t)
    max_ex = []
    for name in names:
        pic_path = os.path.join(path, name)
        img = cv2.imread(pic_path, 0)
        # imshow(template_t)
        # show()
        res = cv2.matchTemplate(img, template_t, cv2.TM_CCOEFF)
        plt.imshow(res, cmap='gray')
        plt.show()
        print(np.max(res))
        print(cv2.minMaxLoc(res))
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # cv2.rectangle(img, min_loc, max_loc, (0, 255, 0), 3)
        cv2.circle(img, max_loc, 20, (0, 0, 255), -1)
        cv2.imwrite('data.jpg', img)
        # print(np.max(res))
        max_ex.append(np.max(res))

    print("-------------------------------------------")
    print(count)
    print(np.max(max_ex))
    print(np.min(max_ex))
    print(np.mean(max_ex))
    print(keyPoints)
    if keyPoints > 600:
        if max(max_ex) > max_tem and min(max_ex) > min_tem:
            max_tem = max(max_ex)
            min_tem = min(max_ex)
            tempalte = rect
    else:
        continue

threshold = max_tem - 0.05

cv2.imwrite('./data/template/img.jpg', canvas)
cv2.imwrite('./data/template/template3.jpg', img_r[tempalte[0][1]:tempalte[1][1], tempalte[0][0]:tempalte[1][0]])
with open('./data/template.txt', 'a') as f:
    f.write('\n')
    f.write('template.jpg' + ' ' + str(tempalte[0][0]) + ' ' + str(tempalte[0][1]) + ' ' + str(width - tempalte[1][0]) + ' ' + str(height - tempalte[1][1]) + ' ' + str(threshold))
    f.close()

with open('./data/template_SIFT.txt', 'a') as f:
    f.write('\n')
    f.write('template.jpg' + ' ' + str(tempalte[0][0]) + ' ' + str(tempalte[0][1]) + ' ' + str(tempalte[1][0]) + ' ' + str(tempalte[1][1]) + ' ' + str(width) + ' ' + str(height))
    f.close()


