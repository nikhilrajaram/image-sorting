import numpy as np
import cv2


class ImageHistogram:
    def __init__(self, filepath, resize_dim):
        self.image = cv2.cvtColor(cv2.resize(cv2.imread(filepath), resize_dim), cv2.COLOR_RGB2HSV)
        self.crops = self.get_crops()
        self.hists = self.get_histograms()

    def get_crops(self):
        crops = []
        for i in range(3):
            for j in range(3):
                crops.append(self.image[(200 * i):(200 * (i + 1)), (200 * j):(200 * (j + 1)), :])
        return np.array(crops)

    def get_histograms(self):
        return [cv2.calcHist([self.crops[i]], [0, 1, 2], None, [180, 256, 256], [0, 180, 0, 256, 0, 256])
                for i in range(9)]

    def get_hists_diff(self, o, method):
        return np.sum([cv2.compareHist(self.hists[i], o.hists[i], method) for i in range(9)])
