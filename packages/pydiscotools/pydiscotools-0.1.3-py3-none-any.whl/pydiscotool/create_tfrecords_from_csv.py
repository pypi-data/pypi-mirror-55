import sys
import tensorflow as tf
import pandas as pd


def create(input_csv_file, output_file_path):
    try:
        print("Reading csv file...")
        csv = pd.read_csv(input_csv_file)
        headers = csv.columns.values
        print("{} column headers found.".format(len(headers)))
        # print(headers)
        print("Writing tfrecords file...")
        c = 0
        with tf.python_io.TFRecordWriter(output_file_path) as writer:
            for row in csv.values:
                features_dict = {}
                for i in range(headers.size):
                    float_list = [row[i]]
                    tf_float_list = tf.train.FloatList(value=(float_list))
                    feature = tf.train.Feature(float_list=tf_float_list)
                    features_dict[headers[i]] = feature
                features = tf.train.Features(feature=features_dict)
                example = tf.train.Example(features=features)
                writer.write(example.SerializeToString())
                c += 1
        print("{} rows imported successfully.".format(c))
    except FileNotFoundError:
        sys.exit("Input File not found.")
    except pd.errors.EmptyDataError:
        sys.exit("Invalid csv file.")
