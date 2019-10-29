import cv2
from graph import BiGraph, all_connected_components
from bitarray import bitarray
from bbox.bbox import BoundingBox
import matplotlib.pyplot as plt

X, Y = 0, 1


class GridLookUp:
    def __init__(self, h, w):
        self._h = h
        self._w = w

    def __len__(self):
        return self._h * self._w

    def to2d(self, d):
        if d >= len(self):
            raise ValueError()
        return d // self._w, d % self._w

    def to1d(self, d0, d1):
        if d1 >= self._w or d0 >= self._h:
            raise ValueError()
        return self._w * d0 + d1


def boundary(lp):
    initial_x, initial_y = lp[0][X], lp[0][Y]
    min_x, max_x = initial_x, initial_x
    min_y, max_y = initial_y, initial_y
    for x, y in lp:
        if min_x > x:
            min_x = x
        if max_x < x:
            max_x = x
        if min_y > y:
            min_y = y
        if max_y < y:
            max_y = y
    return BoundingBox((min_x, min_y), (max_x, max_y))


if __name__ == '__main__':
    img = cv2.imread("gray.jpg")
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    l, w = gray_img.shape

    gl = GridLookUp(l, w)
    barray = bitarray(l * w)
    for i in range(l):
        for j in range(w):
            barray[gl.to1d(i, j)] = gray_img[i, j] > 200

    bg = BiGraph(l * w)
    for i in range(l - 1):
        for j in range(w - 1):
            d = gl.to1d(i, j)
            d0 = gl.to1d(i + 1, j)
            d1 = gl.to1d(i, j + 1)
            if barray[d]:
                if barray[d0]:
                    bg.bond(d, d0)
                if barray[d1]:
                    bg.bond(d, d1)

    boxes = []
    for cc in all_connected_components(bg):
        points = [gl.to2d(d) for d in cc]
        points = [(d[1], d[0]) for d in points]
        b = boundary(points)
        b = b.scale(0.2, 0, gray_img.shape)
        cv2.rectangle(img, *(b.to_opencv_format()), (255, 0, 0), 2)
        boxes.append(b)
    print(boxes)

    bg = BiGraph(len(boxes))
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if boxes[i].overlap(boxes[j]):
                bg.bond(i, j)

    print(all_connected_components(bg))

    for cc in all_connected_components(bg):
        b = boundary([p for x in cc
                      for p in boxes[x].to_opencv_format()
                      ])
        cv2.rectangle(img, *(b.to_opencv_format()), (0, 255, 0), 2)

    plt.imshow(img)
    plt.show()
