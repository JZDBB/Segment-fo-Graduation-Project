import cv2
import numpy as np
from matplotlib import pyplot as plt

template = cv2.imread('temple.jpg', 0)
img = cv2.imread('test1.jpg', 0)
img2 = img.copy()
w, h = template.shape[::-1]
print(w, h)

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

for meth in methods:
    img = img2.copy()
    #exec 语句用来执行储存在字符串或文件中的Python 语句。
    # 例如，我们可以在运行时生成一个包含Python 代码的字符串，然后使用exec 语句执行这些语句。
    #eval 语句用来计算存储在字符串中的有效Python 表达式
    method = eval(meth)
    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(min_loc, min_val, max_loc, max_val)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc

    print(top_left)
    bottom_right = (top_left[0] + w + 5, top_left[1] + h + 5)
    cv2.rectangle(img, top_left, bottom_right, 0, 10)
    plt.subplot(121), plt.imshow(res, cmap='gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(img, cmap='gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()

