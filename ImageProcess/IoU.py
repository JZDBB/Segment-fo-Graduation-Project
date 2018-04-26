from ImageProcess import get_angle

def calculateIoU(candidateBound, groundTruthBound):
    cx1 = candidateBound[0]
    cy1 = candidateBound[1]
    cx2 = candidateBound[2]
    cy2 = candidateBound[3]

    gx1 = groundTruthBound[0]
    gy1 = groundTruthBound[1]
    gx2 = groundTruthBound[2]
    gy2 = groundTruthBound[3]

    carea = (cx2 - cx1) * (cy2 - cy1) #C的面积
    garea = (gx2 - gx1) * (gy2 - gy1) #G的面积

    x1 = max(cx1, gx1)
    y1 = max(cy1, gy1)
    x2 = min(cx2, gx2)
    y2 = min(cy2, gy2)
    w = max(0, x2 - x1)
    h = max(0, y2 - y1)
    area = w * h #C∩G的面积

    iou = area / (carea + garea - area)

    return iou


def Polygonal_IOU(img, poly1, poly2):
    h, w = img.shape[:2]
    count1 = 0
    count2 = 0
    count_all = 0
    for x in range(w):
        for y in range(h):
            if isPointinPolygon([x, y], poly1):
                count1 += 1
                if isPointinPolygon([x, y], poly2):
                    count2 += 1
                    count_all += 1
            elif isPointinPolygon([x, y], poly2):
                count2 += 1
            else:
                pass

    iou = count_all/(count1 + count2 - count_all)
    return iou


# def Polygonal_IOU(img, polylist1, polylist2):
#     h, w = img.shape[:2]
#     count1 = 0
#     count2 = 0
#     count_all = 0
#     for x in range(w):
#         for y in range(h):
#             if isPointinPolygon([x, y], polylist1[i]):
#                 count1 += 1
#                 if isPointinPolygon([x, y], poly2):
#                     count2 += 1
#                     count_all += 1
#             elif isPointinPolygon([x, y], poly2):
#                 count2 += 1
#             else:
#                 pass
#
#     iou = count_all/(count1 + count2 - count_all)
#     return iou


def isPointinPolygon(point, rangelist):
    # 判断是否在外包矩形内，如果不在，直接返回false
    lnglist = []
    latlist = []
    for i in range(len(rangelist)-1):
        lnglist.append(rangelist[i][0])
        latlist.append(rangelist[i][1])
    # print(lnglist, latlist)
    maxlng = max(lnglist)
    minlng = min(lnglist)
    maxlat = max(latlist)
    minlat = min(latlist)
    # print(maxlng, minlng, maxlat, minlat)
    if (point[0] > maxlng or point[0] < minlng or
        point[1] > maxlat or point[1] < minlat):
        return False
    count = 0
    point1 = rangelist[0]
    for i in range(1, len(rangelist)):
        point2 = rangelist[i]
        if (point[0] == point1[0] and point[1] == point1[1]) or (point[0] == point2[0] and point[1] == point2[1]):
            # print("在顶点上")
            return True
        # 判断线段两端点是否在射线两侧 不在肯定不相交 射线（-∞，lat）（lng,lat）
        if (point1[1] < point[1] and point2[1] >= point[1]) or (point1[1] >= point[1] and point2[1] < point[1]):
            # 求线段与射线交点 再和lat比较
            point12lng = point2[0] - (point2[1] - point[1]) * (point2[0] - point1[0])/(point2[1] - point1[1])
            if (point12lng == point[0]):
                # print("点在多边形边上")
                return True
            if (point12lng < point[0]):
                count +=1
        point1 = point2
    # print(count)
    if count%2 == 0:
        return False
    else:
        return True

