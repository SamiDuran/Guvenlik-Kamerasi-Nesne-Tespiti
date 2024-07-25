import numpy as np
import tensorflow as tf
import cv2
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
import os

MODEL_NAME = 'ssd_mobilenet_v2_coco_2018_03_29'
PATH_TO_CKPT = os.path.join(MODEL_NAME, 'frozen_inference_graph.pb')
PATH_TO_LABELS = 'dataset/classes.pbtxt'
NUM_CLASSES = 90

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

sess = tf.compat.v1.Session(graph=detection_graph)

def detector(frame):
    image_np_expanded = np.expand_dims(frame, axis=0)

    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})



    detected_classes = np.squeeze(classes).astype(np.int32)
    detected_scores = np.squeeze(scores)

    class_name = None
    for i in range(len(detected_classes)):
        if detected_scores[i] > 0.6:
            class_id = detected_classes[i]
            if class_id in category_index:
                class_name = category_index[class_id]['name']
                # Sadece 1 veya 2 olan sınıfları işaretleyin
                if class_id == 1 or class_id == 2:
                    ymin, xmin, ymax, xmax = boxes[0, i]  # Kutu koordinatlarını al
                    vis_util.draw_bounding_box_on_image_array(
                        frame,
                        ymin,
                        xmin,
                        ymax,
                        xmax,
                        color='blue',
                        thickness=1,
                        display_str_list=[class_name],
                        use_normalized_coordinates=True
                    )

    return frame, class_name