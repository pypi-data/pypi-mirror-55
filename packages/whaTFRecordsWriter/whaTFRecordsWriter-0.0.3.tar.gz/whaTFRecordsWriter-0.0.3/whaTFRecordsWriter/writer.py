import os
import tensorflow as tf
from whaTFRecordsWriter.preprocessing import load_raw_image
from tqdm import tqdm
from multiprocessing import Pool


class Writer():
    def __init__(self, filename='data.tfrecords', num_writers = 1, writes_per_tfrecords = 1000):
        if filename == '' or not isinstance(filename, str):
            raise ValueError('Invalid given filename: %s' % filename)
        if not isinstance(num_writers, int) or num_writers < 1:
            raise ValueError('Invalid given num_writers: %s' % num_writers)
        if not isinstance(writes_per_tfrecords, int) or writes_per_tfrecords < 1:
            raise ValueError('Invalid given num_writers: %s' % writes_per_tfrecords)
        self.filename = filename
        self.writer = None
        self.writes_per_tfrecords = writes_per_tfrecords
        self.num_writes = 0
        self.num_tfrecords = 0

    def init_writer(self):
        self.writer = tf.io.TFRecordWriter(self.filename)

    def create_new_writer(self):
        self.writer.close()
        self.writer = tf.io.TFRecordWriter(self.filename.replace('.tfrecords', '_' + str(self.num_tfrecords) + '.tfrecords'))
        self.num_writes = 0
        self.num_tfrecords += 1

    def write(self, data):
        if data == None:
            raise ValueError('Invalid given data: %s' % type(data))
        if self.writer == None:
            self.init_writer()
        self.num_writes += 1
        if (self.num_writes - self.writes_per_tfrecords) == 1:
            self.create_new_writer()
        self.writer.write(tf.train.Example(
            features=tf.train.Features(feature=data)).SerializeToString())


def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

def write_images_folder(tfrecord_filename, folder, num_writers = 1, writes_per_tfrecords = 1000000):
    if not isinstance(folder, str) or not os.path.exists(folder):
        raise ValueError('Invalid given folder: %s' % folder)
    if not isinstance(tfrecord_filename, str):
        raise ValueError('Invalid given tfrecord_filename: %s' % tfrecord_filename)
    my = Writer(tfrecord_filename, writes_per_tfrecords = writes_per_tfrecords)
    for i in tqdm(listdir_fullpath(folder)):
        my.write(load_raw_image(i, 'image'))