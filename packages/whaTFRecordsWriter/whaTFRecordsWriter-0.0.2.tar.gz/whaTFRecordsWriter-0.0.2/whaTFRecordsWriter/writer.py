import os
import tensorflow as tf
from whaTFRecordsWriter.encoders import encode_bytes

class Writer():
    def __init__(self, filename='data.tfrecords'):
        if filename == '' or not isinstance(filename, str):
            raise ValueError('Invalid given filename: %s' % filename)
        self.filename = filename
        self.encoding_features = {}
        self.decoding_features = {}
        self.preprocessing_feature = {}

    def addfeature(self, label, feature, feature_len=tf.io.FixedLenFeature, feature_tf_type=tf.string, preporcessing=None):
        if label == '' or not isinstance(label, str):
            raise ValueError('Invalid given label: %s' % label)
        if not isinstance(feature, type(encode_bytes)):
            raise ValueError('Invalid given feature: %s' % feature)
        if label in self.encoding_features:
            raise ValueError('Label - %s - already exists' % label)
        if label in self.encoding_features:
            raise ValueError('Label - %s - already exists' % label)
        self.encoding_features[label] = feature
        self.preprocessing_feature[label] = preporcessing
        self.decoding_features[label] = feature_len([], feature_tf_type)

    def write(self, data_dir):
        if data_dir == '' or not os.path.exists(data_dir):
            raise ValueError('Invalid given directory: %s' % data_dir)
        with tf.io.TFRecordWriter(self.filename) as writer:
            for i in self.listdir_fullpath(data_dir):
                new_features = self.encoding_features.copy()
                for j in new_features.keys():
                    data = i
                    if self.preprocessing_feature[j] != None:
                        data= self.preprocessing_feature[j](data)
                    new_features[j] = self.encoding_features[j](data)
                writer.write(tf.train.Example(features=tf.train.Features(feature=new_features)).SerializeToString())

    @staticmethod
    def listdir_fullpath(d):
        return [os.path.join(d, f) for f in os.listdir(d)]