import numpy as np
import cv2
import PIL.Image as im


def load_resized_img(filepath, dim):
    I = cv2.resize(cv2.imread(filepath), dim)
    return cv2.cvtColor(I, cv2.COLOR_RGB2HSV)


def get_crops(img):
    crops = []
    for i in range(3):
        for j in range(3):
            crops.append(img[(200*i):(200*(i+1)), (200*j):(200*(j+1)), :])
    return np.array(crops)


def get_histogram(img):
    return cv2.calcHist([img[:, :, 0:3]], [0, 1, 2], None, [180, 256, 256], [0, 180, 0, 256, 0, 256])


def get_hist_diff(img_1, img_2, method):
    img_1_crops = get_crops(img_1)
    img_2_crops = get_crops(img_2)

    img_1_hists = [get_histogram(img_1_crops[i]) for i in range(9)]
    img_2_hists = [get_histogram(img_2_crops[i]) for i in range(9)]

    return np.sum([cv2.compareHist(img_1_hists[i], img_2_hists[i], method) for i in range(9)])


if __name__ == '__main__':
    # very similar
    I1 = load_resized_img('../img/IMG_20180713_143820_2.jpg', (600, 600))
    I2 = load_resized_img('../img/IMG_20180713_143819_2.jpg', (600, 600))

    # somewhat similar
    I3 = load_resized_img('../img/IMG_20180713_150338.jpg', (600, 600))
    I4 = load_resized_img('../img/IMG_20180713_150328.jpg', (600, 600))

    # dissimilar
    I5 = load_resized_img('../img/20160708_140405.jpg', (600, 600))
    I6 = load_resized_img('../img/paris_general_000076.jpg', (600, 600))

    print(get_hist_diff(I1, I2, cv2.HISTCMP_CHISQR))
    print(get_hist_diff(I3, I4, cv2.HISTCMP_CHISQR))
    print(get_hist_diff(I5, I6, cv2.HISTCMP_CHISQR))








