import tensorflow as tf
from whaTFRecordsWriter.encoders import encode_bytes

def load_raw_image(image_addr, name):
    file = open(image_addr, 'rb')
    image = file.read()
    file.close()
    return {name: encode_bytes(tf.compat.as_bytes(image))}