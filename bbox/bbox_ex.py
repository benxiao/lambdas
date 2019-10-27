import cv2
import matplotlib.pyplot as plt
from get_bbox import *

# print(bfs(square, (5,5), (0, 2)))
img = cv2.imread("gray.jpg")
gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# print(gray_img.flatten().min(), gray_img.flatten().max())
# print(np.unique(gray_img.flatten()))
lst = gray_img.tolist()
bs = bboxes(gray_img, gray_img.shape)
bs = [b for b in bs if b.area() > 20]
bs = [b.scale(0.2, 0.1, gray_img.shape) for b in bs]
for b in bs:
    cv2.rectangle(img, *(b.to_opencv_format()), (255, 0, 0), 1)


print(bs[0].overlap(bs[1]))
print(bs[0].overlap(bs[2]))
print()





plt.imshow(img)
plt.show()
