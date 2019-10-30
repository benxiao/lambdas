from typing import *

D0, D1 = 0, 1
Point = Tuple[int, int]


"""
Point d0: Dimension 0, d1: Dimension 1

"""


class BoundingBox:
    def __init__(self, top_left: Point, bottom_right: Point):
        self._top_left = top_left
        self._bottom_right = bottom_right
        # if not self.validate():
        #     print(self._top_left)
        #     print(self._bottom_right)
        #     raise ValueError("invalid boundbox")

    def validate(self):
        return self._bottom_right[D0] >= self._top_left[D0] and self._bottom_right[D1] >= self._top_left[D1]

    def __str__(self):
        return f"BoundingBox({self._top_left}, {self._bottom_right})"

    __repr__ = __str__

    def to_opencv_format(self):
        return self.get_top_left(), self.get_bottom_right()

    def get_top_left(self):
        return self._top_left

    def get_bottom_right(self):
        return self._bottom_right

    def get_bottom_left(self):
        return self.get_bottom_right()[D0], self.get_top_left()[D1]

    def get_top_right(self):
        return self._bottom_right[D0], self._top_left[D1]

    def width(self):
        return self._bottom_right[D0] - self._top_left[D0]

    def height(self):
        return self._bottom_right[D1] - self._top_left[D1]

    def shape(self):
        return self.height(), self.width()

    def area(self):
        return self.width() * self.height()

    def center(self):
        d0, d1 = self.get_top_left()
        return d0 + self.height() // 2,  d1 + self.width() // 2

    def scale(self, w_factor, h_factor, context):
        context_height, context_width = context
        width = self.width()
        height = self.height()
        top_left = self.get_top_left()
        bottom_right = self.get_bottom_right()
        top_left_d0 = max(top_left[D0] - height * h_factor, 0)
        top_left_d1 = max(top_left[D1] - width * w_factor, 0)
        bottom_right_d0 = min(bottom_right[D0] + height * h_factor, context_width)
        bottom_right_d1 = min(bottom_right[D1] + width * w_factor, context_height)
        return BoundingBox((int(top_left_d0), int(top_left_d1)),
                           (int(bottom_right_d0), int(bottom_right_d1)))

    # maybe there are bugs
    def overlap(self, other):
        # how to test this
        a, b = self, other
        # a always stays on the left
        if a.get_top_left()[D1] > b.get_top_left()[D1]:
            a, b = b, a
        x0, y0 = a.get_bottom_right()
        x1, y1 = b.get_top_left()
        if x0 > x1 and y0 > y1:
            return True
        x0, y0 = a.get_top_right()
        x1, y1 = b.get_bottom_left()
        return x0 > x1 and y1 > y0


if __name__ == '__main__':
    a = BoundingBox((0, 0), (400, 400))
    b = BoundingBox((400,400), (401,401))
    print(a.overlap(b))

