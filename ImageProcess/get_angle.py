

def get_cos(pt1, pt2, pt3):
    x1, y1 = float(pt1[0]), float(pt1[1])
    x2, y2 = float(pt2[0]), float(pt2[1])
    x3, y3 = float(pt3[0]), float(pt3[1])
    sqrt_a = (x2 - x1) ** 2 + (y2 - y1) ** 2
    sqrt_b = (x2 - x3) ** 2 + (y2 - y3) ** 2
    sqrt_c = (x3 - x1) ** 2 + (y3 - y1) ** 2
    cos_theta = (sqrt_a + sqrt_b - sqrt_c)/((2 * (sqrt_a ** 0.5) * (sqrt_b ** 0.5))+0.000001)

    return cos_theta
