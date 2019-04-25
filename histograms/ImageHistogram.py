import numpy as np
import cv2


class ImageHistogram:
    def __init__(self, filename, resize_dim, save_memory=False):
        self.filename = filename
        self.height, self.width = resize_dim
        self.crop_height, self.crop_width = int(self.height / 3), int(self.width / 3)
        self.rgb_image = cv2.cvtColor(cv2.resize(cv2.imread(self.filename), resize_dim), cv2.COLOR_RGB2BGR)
        self.hsv_image = cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2HSV)
        self.features = self.get_features()
        self.crops = self.get_crops()
        self.hists = self.get_histograms()

        if save_memory:
            del self.rgb_image
            del self.hsv_image
            del self.features

    @staticmethod
    def rescale(x, y_min, y_max):
        x_0_1 = (x - np.min(x)) / (np.max(x) - np.min(x))
        return x_0_1 * (y_max - y_min) + y_min

    @staticmethod
    def swap_axes(x, *args):
        for ax1, ax2 in zip(args[:-1], args[1:]):
            x = np.swapaxes(x, ax1, ax2)

        return x

    @staticmethod
    def compare_hists(h1, h2, n_features, method, feature_weights):
        assert h1.shape == h2.shape, "histograms are not comparable"
        assert len(feature_weights) == n_features, "feature_weights must be of length n_features"

        if len(h1.shape) == 1:
            h1 = h1.reshape(n_features, 255).astype(np.float32)
            h2 = h2.reshape(n_features, 255).astype(np.float32)

        s = 0
        for i in range(h1.shape[0]):
            s += feature_weights[i] * cv2.compareHist(h1[i], h2[i], method)

        return s

    def get_features(self):
        features = np.zeros((15, self.height, self.width))

        # hsv features
        hsv = self.swap_axes(self.hsv_image, 0, 2, 1)
        features[0, :, :] = self.rescale(hsv[0, :, :], 0, 255)
        features[1, :, :] = hsv[1, :, :]
        features[2, :, :] = hsv[2, :, :]

        i = 3
        for channel in range(3):
            for theta in [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]:
                gabor = cv2.getGaborKernel((5, 5), 3, theta, 5, 0.25, 0)
                features[i, :, :] = self.rescale(cv2.filter2D(self.rgb_image[:, :, channel], -1, gabor), 0, 255)
                i += 1

        return np.array(features, dtype=np.float32)

    def get_crops(self):
        crops = np.zeros((9, 15, self.crop_height, self.crop_width))
        for i in range(3):
            for j in range(3):
                crops[3 * i + j] = self.features[:, (self.crop_height * i):(self.crop_height * (i + 1)),
                                                    (self.crop_width * j):(self.crop_width * (j + 1))]
        return crops.astype(np.float32)

    def get_histograms(self):
        hists = np.zeros((3 + 9 * (3 + 12), 255))

        hists[0, :] = cv2.calcHist([self.hsv_image[:, :, 0]], [0], None, [255], [0, 255]).reshape(1, -1)[0]
        hists[1, :] = cv2.calcHist([self.hsv_image[:, :, 1]], [0], None, [255], [0, 255]).reshape(1, -1)[0]
        hists[2, :] = cv2.calcHist([self.hsv_image[:, :, 2]], [0], None, [255], [0, 255]).reshape(1, -1)[0]

        for n in range(15):
            hists[3 + 9 * n:3 + 9 * (n + 1), :] = np.stack(
                [cv2.calcHist([self.crops[i, n, :, :]], [0], None, [255], [0, 255]).reshape(1, -1)[0]
                 for i in range(9)])

        return hists.astype(np.float32)
