from typing import *

X, Y = 0, 1
Point = Tuple[int, int]


class BoundingBox:
    def __init__(self, top_left: Point, bottom_right: Point):
        self.top_left = top_left
        self.bottom_right = bottom_right
        if self.bottom_right[X] < self.top_left[X] and self.bottom_right[Y] < self.top_left[Y]:
            raise ValueError("invalid boundbox")

    def to_opencv_format(self):
        return self.top_left, self.bottom_right

    def get_top_left(self):
        return self.top_left

    def get_bottom_right(self):
        return self.bottom_right

    def get_bottom_left(self):
        return self.top_left[X], self.bottom_right[Y]

    def get_top_right(self):
        return self.bottom_right[X], self.top_left[Y]

    def width(self):
        return self.bottom_right[X] - self.top_left[X]

    def height(self):
        return self.bottom_right[Y] - self.top_left[Y]

    def shape(self):
        return self.width(), self.height()

    def area(self):
        return self.width() * self.height()

    def center(self):
        x0, y0 = self.get_top_left()
        return x0 + self.width() // 2,  y0 + self.height() // 2

    def scale(self, w_factor, h_factor, context):
        context_width, context_height = context
        width = self.width()
        height = self.height()
        top_left = self.get_top_left()
        bottom_right = self.get_bottom_right()
        top_left_x = max(top_left[X] - width * w_factor, 0)
        top_left_y = max(top_left[Y] - height * h_factor, 0)
        bottom_right_x = min(bottom_right[X] + width * w_factor, context_width)
        bottom_right_y = min(bottom_right[Y] + height * h_factor, context_height)
        return BoundingBox((int(top_left_x), int(top_left_y)),
                           (int(bottom_right_x), int(bottom_right_y)))

    def merge(self, other):
        top_left0 = self.get_top_left()
        top_left1 = other.get_top_left()
        bottom_right0 = self.get_bottom_right()
        bottom_right1 = other.get_bottom_right()
        new_top_left = (
            min(top_left0[X], top_left1[X]),
            min(top_left0[Y], top_left1[Y])
        )
        new_bottom_right = (
            max(bottom_right0[X], bottom_right1[X]),
            max(bottom_right0[Y], bottom_right1[Y])
        )
        return BoundingBox(new_top_left, new_bottom_right)

    def overlap(self, other):
        a, b = self, other
        # a always stays on the left
        if a.top_left[X] > b.top_left[Y]:
            a, b = b, a
        x0, y0 = a.get_bottom_right()
        x1, y1 = b.get_top_left()
        if x0 > x1 and y0 > y1:
            return True
        x0, y0 = a.get_top_right()
        x1, y1 = b.get_bottom_left()
        return x0 > x1 and y1 > y0


if __name__ == '__main__':
    pass

