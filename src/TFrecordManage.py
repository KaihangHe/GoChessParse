#!/usr/bin/python3
# code by nicapoet
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image


def readTFrecord(tfrecord_path):
    filename_queue = tf.train.string_input_producer([tfrecord_path], )
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)

    dataset = tf.parse_single_example(serialized_example,                        features={'label': tf.FixedLenFeature([], tf.int64),'img_raw': tf.VarLenFeature( tf.string)})
    # image = tf.decode_raw(dataset['img_raw'], tf.int64)
    # image = tf.reshape(image, [300, -1])
    label = tf.cast(dataset['label'], tf.int64)
    print(serialized_example)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
        for i in range(20):
            label = sess.run([label])
            print(label)
            # img=Image.fromarray(example_image,'RGB')
            # img.save('../1.jpg')
            # print(example_label)
        coord.request_stop()
        coord.join(threads)

if __name__ == '__main__':
    readTFrecord('../data/train.record')
