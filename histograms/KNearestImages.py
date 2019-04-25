import os
import numpy as np
import cv2
from sklearn.neighbors import NearestNeighbors as KNN
from ImageHistogram import ImageHistogram


class KNearestImages:
    def __init__(self, IH, k, weights=[0.4 / 3] * 3 + [0.3 / 27] * 27 + [0.3 / 108] * 108):
        self.IH = IH
        self.weights = weights

        if 'hists.npy' not in os.listdir('data/'):
            self.get_hists()

        self.hists = np.load('data/hists.npy', allow_pickle=True)

        self.nn = KNN(k, metric=ImageHistogram.compare_hists, metric_params={'n_features': 138,
                                                                             'method': cv2.HISTCMP_BHATTACHARYYA,
                                                                             'feature_weights': self.weights})
    def fit(self):
        self.nn.fit(self.hists)

    def kneighbors(self):
        return self.nn.kneighbors([self.IH.hists])
