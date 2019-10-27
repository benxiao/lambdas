from collections import deque
from typing import *
import cv2
import numpy as np
import matplotlib.pyplot as plt
from bbox import BoundingBox

Point = Tuple[int, int]
TopLeft, BottomRight = Point, Point
Square = np.ndarray
Dimension = Tuple[int, int]
X, Y = 0, 1


def bfs(square: Square, dimension: Dimension, start: Point, threshold) -> List[Point]:
    l, w = dimension
    q = deque()
    q.append(start)
    seen = {start}
    lst = []
    while q:
        x, y = q.popleft()
        lst.append((x, y))
        # up
        if (x - 1 >= 0) and square[y, x - 1] > threshold:
            if (x - 1, y) not in seen:
                q.append((x - 1, y))
                seen.add((x - 1, y))
        # bottom
        if (x + 1 < w) and square[y, x + 1] > threshold:
            if (x + 1, y) not in seen:
                q.append((x + 1, y))
                seen.add((x + 1, y))
        # left
        if (y - 1 >= 0) and square[y - 1, x] > threshold:
            if (x, y - 1) not in seen:
                q.append((x, y - 1))
                seen.add((x, y - 1))
        # right
        if (y + 1 < l) and square[y + 1, x] > threshold:
            if (x, y + 1) not in seen:
                q.append((x, y + 1))
                seen.add((x, y + 1))
    return lst


def bbox(lp: List[Point]):
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


def bboxes(square: Square, dimension: Dimension, threshold=200):
    l, w = dimension
    candidates = []
    for i in range(w):
        for j in range(l):
            if square[j, i] > 200:
                candidates.append((i, j))
    lst = []
    while candidates:
        p = candidates.pop()
        lp = bfs(square, dimension, p, threshold=threshold)
        lst.append(bbox(lp))
        for p in lp:
            if p in candidates:
                candidates.remove(p)
    return lst


def bbox_filter_size(bs: List[BoundingBox], minimum_size=10):
    return [b for b in bs if b.area() > minimum_size]



if __name__ == '__main__':
    # print(bfs(square, (5,5), (0, 2)))
    img = cv2.imread("gray.jpg")
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # print(gray_img.flatten().min(), gray_img.flatten().max())
    # print(np.unique(gray_img.flatten()))
    lst = gray_img.tolist()
    bs = bboxes(gray_img, gray_img.shape)
    bs = bbox_filter_size(bs, minimum_size=20)
    bs = [b.scale(0.2, 0.1, gray_img.shape) for b in bs]
    for b in bs:
        cv2.rectangle(img, *(b.to_opencv_format()), (255, 0, 0), 1)



    plt.imshow(img)
    plt.show()
