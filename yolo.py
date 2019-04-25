import cv2
import numpy as np
import os

# https://www.arunponnusamy.com/yolo-object-detection-opencv-python.html
# weights: https://pjreddie.com/media/files/yolov3.weights


def get_classes(file):
    # read class names from text file
    classes = None
    with open(file, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    return classes


def get_colors(classes):
    # generate different colors for different classes
    return np.random.uniform(0, 255, size=(len(classes), 3))


def get_net(weights_f, cfg_f, im, scl):
    # read pre-trained model and config file
    net = cv2.dnn.readNet(weights_f, cfg_f)

    # create input blob
    blob = cv2.dnn.blobFromImage(im, scl, (416, 416), (0, 0, 0), True, crop=False)

    # set input blob for the network
    net.setInput(blob)

    return net


def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


# function to draw bounding box on the detected object with class name
def draw_bounding_box(img, class_id, colors, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])
    color = colors[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def show_image(image, net, colors, Width, Height, resize):
    # run inference through the network
    # and gather predictions from output layers
    outs = net.forward(get_output_layers(net))

    # initialization
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    # for each detetion from each output layer
    # get the confidence, class id, bounding box params
    # and ignore weak detections (confidence < 0.5)
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                print(detection[0:4])
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    # apply non-max suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    # go through the detections remaining
    # after nms and draw bounding box

    image = cv2.resize(image, (int(resize * Width), int(resize * Height)))

    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]

        draw_bounding_box(image, class_ids[i], colors, confidences[i],
                          round(resize*x), round(resize*y), round(resize*(x+w)), round(resize*(y+h)))

    print()

    # display output image
    cv2.imshow("object detection", image)

    # wait until any key is pressed
    cv2.waitKey()

    # save output image to disk
    # cv2.imwrite("object-detection.jpg", image)
    print("Classes:")
    print([classes[i] for i in list(set(class_ids))])

    # release resources
    cv2.destroyAllWindows()


if __name__ == '__main__':
    img = "interface/static/PhotoSorter_images/paris_general_000008.jpg"
    weights_file = "yolo/yolov3.weights"
    cfg_file = "yolo/yolov3.cfg"
    classes_file = "yolo/yolov3.txt"

    # compare images

    folder = "interface/static/PhotoSorter_images/"
    img_names = os.listdir(folder)
    imgs = [folder + file for file in img_names]

    for img in imgs:
        image = cv2.imread(img)

        w = image.shape[1]
        h = image.shape[0]
        scale = 0.00392

        classes = get_classes(classes_file)
        colors = get_colors(classes)
        net = get_net(weights_file, cfg_file, image, scale)

        if 960 / w > 600 / h:
            c = 960 / w
        else:
            c = 600 / h

        show_image(image, net, colors, w, h, c)



