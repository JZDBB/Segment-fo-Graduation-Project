import cv2
import numpy as np
import matplotlib.pyplot as plt



a = np.array([[[10,20], [100,20], [100,200], [10,200]]], dtype = np.int32)
b = np.array([[[100,100], [200,230], [150,200], [100,220]]], dtype = np.int32)
print(a.shape)
im = np.zeros([240, 320], dtype = np.uint8)
cv2.polylines(im, b, 1, 255)
cv2.fillPoly(im, a, 255)
plt.imshow(im, cmap='gray')
plt.show()





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



