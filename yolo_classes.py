import os
import numpy as np
import cv2
import yolo


def get_image_classes(net, classes):
    # run inference through the network
    # and gather predictions from output layers
    outs = net.forward(yolo.get_output_layers(net))

    # initialization
    class_ids = []
    confidences = []

    # for each detetion from each output layer
    # get the confidence, class id, bounding box params
    # and ignore weak detections (confidence < 0.5)
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                class_ids.append(class_id)
                confidences.append(float(confidence))

    # print([classes[i] for i in list(set(class_ids))])
    return [classes[i] for i in list(set(class_ids))]

if __name__ == '__main__':
    weights_file = "yolo/yolov3.weights"
    cfg_file = "yolo/yolov3.cfg"
    classes_file = "yolo/yolov3.txt"

    # compare images

    folder = "interface/static/PhotoSorter_images/"
    img_names = os.listdir(folder)
    imgs = [folder + file for file in img_names]

    with open('yolo/yolo_classes.csv', 'w') as f:
        for img in imgs:
            image = cv2.imread(img)

            classes = yolo.get_classes(classes_file)
            colors = yolo.get_colors(classes)
            scale = 0.00392

            net = yolo.get_net(weights_file, cfg_file, image, scale)

            f.write('{},'.format(img.replace(folder, '')))

            clss = get_image_classes(net, classes)

            for cls in clss[:-1]:
                f.write('{},'.format(cls))

            if clss:
                f.write('{}'.format(clss[-1]))
            else:
                f.write('None')

            f.write('\n')
