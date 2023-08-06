import click
import os
import sys
import tensorflow as tf
import pandas as pd


@click.group()
def main():
    pass


@main.command()
@click.argument('input_csv_file')
@click.argument('output_file_path', required=False)
def create_tfrecords_from_csv(input_csv_file, output_file_path):
    if output_file_path is None:
        output_file_path = os.path.splitext(input_csv_file)[0] + ".tfrecords"
    if not output_file_path.endswith(".tfrecords"):
        output_file_path = output_file_path + ".tfrecords"
    if not os.path.exists(output_file_path):
        try:
            output_file_dir = os.path.dirname(output_file_path)
            os.makedirs(output_file_dir)
        except OSError:
            print("Creation of the directory %s failed" % output_file_dir)
        else:
            print("Successfully created the directory %s" % output_file_dir)

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


if __name__ == '__main__':
    main()
