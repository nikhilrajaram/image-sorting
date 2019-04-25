import os
import numpy as np
import cv2
from sklearn.neighbors import NearestNeighbors as KNN
from ImageHistogram import ImageHistogram


class KNearestImages:
    def __init__(self, k, weights=[0.4 / 3] * 3 + [0.3 / 27] * 27 + [0.3 / 108] * 108):
        self.weights = weights
        self.isFit = False

        with open('data/filenames.txt') as f:
            self.filenames = [_.strip('\n') for _ in f.readlines()]

        if 'hists.npy' not in os.listdir('data/'):
            self.get_hists()

        self.hists = np.load('data/hists.npy', allow_pickle=True)

        self.nn = KNN(k, metric=ImageHistogram.compare_hists, metric_params={'n_features': 138,
                                                                             'method': cv2.HISTCMP_BHATTACHARYYA,
                                                                             'feature_weights': self.weights})

    def fit(self):
        self.nn.fit(self.hists)
        self.isFit = True

    def kneighbors(self, IH):
        assert self.isFit, "model must be fit first"
        dists, idxs = self.nn.kneighbors([IH.hists.flatten()])

        return dists, [self.filenames[idx] for idx in idxs[0]]

    def get_hists(self):
        hists = np.zeros((len(self.filenames), 138*255))

        for i, filename in enumerate(self.filenames):
            hists[i] = ImageHistogram('../img/{}'.format(filename), (450, 450)).hists.flatten()

        np.save('data/hists.npy', hists)
