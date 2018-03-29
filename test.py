import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy import *



"""
python是解析型语言和C++等编译型语言的区别：
编译型：全局变量必须在使用之前定义
解析型：是按照执行顺序编译，因此变量只需在运行顺序前定义即可。
"""

def debug(im):
    im = im.copy()
    im = im.I
    print(type(im))
    print(im)
    return im

img = array([[0, 0, 0],
            [1, 2, 1]])
a = debug(img)
print(img)


"""
    @ read txt data
"""
# with open('./data/template.txt', 'r') as f:
#     data = f.readlines()  # txt中所有字符串读入data
#     for line in data:
#         odom = line.split(' ')  # 将单个数据分隔开存好
#         print(odom)

"""
    @ draw a recotangle (filled and not filled)
"""
# a = np.array([[[10,20], [100,20], [100,200], [10,200]]], dtype = np.int32)
# b = np.array([[[100,100], [200,230], [150,200], [100,220]]], dtype = np.int32)
# print(a.shape)
# im = np.zeros([240, 320], dtype = np.uint8)
# cv2.polylines(im, b, 1, 255)
# cv2.fillPoly(im, a, 255)
# plt.imshow(im, cmap='gray')
# plt.show()





# template = cv2.imread('temple.jpg', 0)
# img = cv2.imread('test.jpg', 0)
# img2 = img.copy()
# w, h = template.shape[::-1]
# print(w, h)


"""
 @ recignize a picture with a sigle object
"""
# methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
#             'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
# for meth in methods:
#     img = img2.copy()
#     #exec 语句用来执行储存在字符串或文件中的Python 语句。
#     # 例如，我们可以在运行时生成一个包含Python 代码的字符串，然后使用exec 语句执行这些语句。
#     #eval 语句用来计算存储在字符串中的有效Python 表达式
#     method = eval(meth)
#     # Apply template Matching
#     res = cv2.matchTemplate(img,template,method)
#
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#     print(min_loc, min_val, max_loc, max_val)
#
#     if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
#         top_left = min_loc
#     else:
#         top_left = max_loc
#     # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
#
#     print(top_left)
#     bottom_right = (top_left[0] + w + 5, top_left[1] + h + 5)
#     cv2.rectangle(img, top_left, bottom_right, 0, 10)


"""
 @ recognize with one more object
"""
# threshold = 0.35
# res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
# loc = np.where(res >= threshold)
# for pt in zip(*loc[::-1]):
#     cv2.rectangle(img, pt, (pt[0] + w + 5, pt[1] + h + 5), 0, 10)


"""
 @ plot result
"""
# from matplotlib import pyplot as plt
# plt.subplot(131),plt.imshow(res,cmap = 'gray')
# plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
# plt.subplot(132),plt.imshow(img,cmap = 'gray')
# plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
# plt.subplot(133),plt.imshow(template,cmap = 'gray')
# plt.title('template'), plt.xticks([]), plt.yticks([])
# plt.show()



