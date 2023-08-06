import tensorflow as tf
def load_image(image_addr):
    file = open(image_addr, 'rb')
    image = file.read()
    file.close()
    return tf.compat.as_bytes(image)