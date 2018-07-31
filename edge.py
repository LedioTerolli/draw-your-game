import cv2
import numpygame as np

'''
from matplotlib import pygameplot as plt

img = cv2.imread('ironman.jpeg', 0)
edges = cv2.Canny(img, 100, 200)

print(edges)

plt.subplot(121), plt.imshow(img, cmap='gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(edges, cmap='gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
'''

X2 = []
X1 = [1, 2, 3]
X2.append(X1)
X3 = [4, 5, 6]
X2.append(X3)
print(X2)
