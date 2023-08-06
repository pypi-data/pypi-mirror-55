# whaTFRecordsWriter

# Overview

Are you having trouble saving your precious data into an easy format for training and testing? Well, you're in luck because with `whaTFRecordsWriter` we are trying to minimize the effort required to simplify your dataset with [TFRecord]('https://www.tensorflow.org/tutorials/load_data/tfrecord'). 

# Installation

Python 3.6+ is required

```Python
pip install whaTFRecordsWriter
```

# Example

## Converting Images with no labels to tfrecords

```python
# 'test.tfrecords' is what you want to name your tfrecords
# 'test_data' is the file directory that has the following structure:
# test_data: /
#       [image_0001.jpg]
#       [image_0002.jpg]
#       [image_000x.jpg]
#       ...
# 'writes_per_tfrecords' is the number of images to save per tfrecord.
import whaTFRecordsWriter as wr
wr.write_images_folder('test.tfrecords', 'test_data', writes_per_tfrecords=10)
```