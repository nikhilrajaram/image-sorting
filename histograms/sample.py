import os
import numpy as np
import cv2
from ImageHistogram import ImageHistogram
from KNearestImages import KNearestImages

if __name__ == '__main__':
    IH = ImageHistogram('../img/0116.jpg', (450, 450))
    knn = KNearestImages(5)

    knn.fit()
    dists, imgs = knn.kneighbors(IH)

    for img in imgs:
        print('open {} {}'.format(IH.filename.replace('../img/', ''), img))
