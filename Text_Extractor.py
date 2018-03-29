# -*- coding: utf-8 -*-

import cv2
import os
import numpy as np
from functools import cmp_to_key

def findContours(img, mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_SIMPLE):
    if cv2.__version__[0] == '2':
        contours2, hierarchy2 = cv2.findContours(img.copy(),mode,method)
    elif cv2.__version__[0] == '3':
        _,contours2, hierarchy2 = cv2.findContours(img.copy(),mode,method)
    return contours2, hierarchy2
    
class Text_Extractor():

    def filterSmallBoxes(self, boxes, minHeight=-1,maxHeight=-1,minWidth=-1,maxWidth=-1):
        '''
        过滤面积小的区域
        :param boxes:区域list
        :param minHeight:最小高度
        :return:区域过滤后的结果list
        '''
        ret = []
        for box in boxes:
            d1 = np.sqrt((box[0, 0] - box[1, 0]) ** 2 + (box[0, 1] - box[1, 1]) ** 2)
            d2 = np.sqrt((box[1, 0] - box[2, 0]) ** 2 + (box[1, 1] - box[2, 1]) ** 2)
            h = 0
            w = 0
            if d1 < d2:
                h = d1
                w = d2
            else:
                h = d2
                w = d1
            if minHeight != -1:
                if h < minHeight:
                    continue
            if maxHeight != -1:
                if h > maxHeight:
                    continue
            if minWidth != -1:
                if w < minWidth:
                    continue
            if maxWidth != -1:
                if h > maxWidth:
                    continue
            ret.append(box)
        return ret

    def getOriginal(self, boxes, M):
        '''
        将坐标还原到原图中
        :param _2dboxes: 当前区域所在位置的list
        :param M:逆变换矩阵
        :return:原图中所有区域位置的list
        '''
        ret = []
        for box in boxes:
            tmp = np.vstack((box.T, np.ones((1, 4))))
            tmp = np.dot(M, tmp)
            tmp = tmp[0:2, :].T
            tmp = tmp.astype(int)
            ret.append(tmp)
        return ret

    def extract(self, im):
        '''
        字段区域截取
        :param im:原始图片
        :return:返还的有序list，按照从左到右，从上到下顺序排列
        '''
        im = im.copy()
        bg_color = np.median(im[np.where(im != (0, 0, 0))])
        im[np.where(im == (0, 0, 0))] = bg_color

        M1 = np.float32([[1, 0, -im.shape[1] / 2],
                         [0, 1, -im.shape[0] / 2], [0, 0, 1]])
        scale = 3000.0 / im.shape[1]
        M2 = np.float32([[scale, 0, 0], [0, scale, 0], [0, 0, 1]])
        im = cv2.resize(im, (3000, int(3000.0 / im.shape[1] * im.shape[0])))
        M3 = np.float32(
            [[1, 0, im.shape[1] / 2], [0, 1, im.shape[0] / 2], [0, 0, 1]])
        M = np.linalg.inv(np.dot(M3, np.dot(M2, M1)))

        gray_img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ave = np.average(gray_img)
        if ave > 128:
            gray_img = 255 - gray_img

        _, binary_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # cv2.namedWindow('binary_img', cv2.WINDOW_NORMAL)
        # cv2.imshow("binary_img", binary_img)
        # element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # mask = cv2.erode(binary_img, element)
        mask = cv2.GaussianBlur(binary_img, (77, 5), 0)
        # cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
        # cv2.imshow("mask", mask)
        contours, hierarchy = findContours(mask,mode=cv2.RETR_TREE)
        show = img.copy()
        boxes = []
        print(len(contours))
        for cnt in contours:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            boxes.append(box)
        boxes = self.filterSmallBoxes(boxes, 20,100,50,800)
        ret_boxes = self.getOriginal(boxes, M)
        for box in boxes:
            cv2.drawContours(show, [box], 0, (255, 0, 0), 5)
        cv2.namedWindow('show', cv2.WINDOW_NORMAL)
        cv2.imshow("show", show)
        return boxes, ret_boxes

    def getImg(self, im, box):
        '''
        获取区域内部的图片
        :param im: 图片
        :param box:区域位置
        :return:截取图片
        '''
        im = im.copy()
        dx1, dy1 = (box[2, 0] - box[1, 0], box[2, 1] - box[1, 1])
        dx2, dy2 = (box[1, 0] - box[0, 0], box[1, 1] - box[0, 1])
        cx = int((box[2, 0] + box[1, 0] + box[0, 0] + box[3, 0]) / 4)
        cy = int((box[2, 1] + box[1, 1] + box[0, 1] + box[3, 1]) / 4)
        dx = 0
        dy = 0
        _dx = 0
        _dy = 0
        if abs(dx2) > abs(dx1):
            dx = dx2
            dy = dy2
            _dx = dx1
            _dy = dy1
        else:
            dx = dx1
            dy = dy1
            _dx = dx2
            _dy = dy2
        if dx < 0:
            dx = -dx
            dy = -dy
        if _dy < 0:
            _dx = -_dx
            _dy = -_dy

        w = np.sqrt(dx ** 2 + dy ** 2)
        h = np.sqrt(_dx ** 2 + _dy ** 2)

        _cos = dx / w
        _sin = dy / w

        M1 = np.float32([[1, 0, -cx], [0, 1, -cy], [0, 0, 1]])
        M2 = np.float32([[_cos, _sin, 0], [-_sin, _cos, 0], [0, 0, 1]])
        M3 = np.float32([[1, 0, w / 2], [0, 1, h / 2], [0, 0, 1]])

        M = np.dot(M3, np.dot(M2, M1))
        im = cv2.warpPerspective(im, M, (int(w), int(h)))

        return im

    def cutImgs(self, im, boxes):
        '''
        获取所有区域的图片
        :param im:图片
        :param boxes:所有区域位置的list
        :return:所有截取区域的图片list
        '''
        im = im.copy()
        imgs = []
        for box in boxes:
            ret_im = self.getImg(im, box)
            ret_im = cv2.cvtColor(ret_im, cv2.COLOR_BGR2GRAY)
            ret_im = 255 - ret_im
            imgs.append(ret_im)
        return imgs

    def cut(self, img):
        '''
        提取图片中的字段区域
        :param img:图片
        :return:提取区域图片和位置的list,
        '''
        boxes, ret_boxes = self.extract(img.copy())
        ret_imgs = self.cutImgs(img, ret_boxes)
        return ret_imgs, ret_boxes

#
if __name__ == '__main__':

    TE = Text_Extractor()
    path = './2.jpg'
    img = cv2.imread(path)
    cv2.namedWindow('src', cv2.WINDOW_NORMAL)
    cv2.imshow('src',img)
    ret_imgs, ret_boxes = TE.cut(img)
    print(ret_boxes, "ok")
    for seq in ret_imgs:
        cv2.namedWindow('seq', cv2.WINDOW_NORMAL)
        cv2.imshow("seq",seq)
        cv2.waitKey(0)
