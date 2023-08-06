import click
from pydiscotools import tfrecords_creator


@click.group()
def main():
    pass


@main.command()
@click.argument('input_csv_file')
@click.argument('output_file_path', required=False)
def create_tfrecords_from_csv(input_csv_file, output_file_path):
    tfrecords_creator.create_tfrecords_from_csv(input_csv_file, output_file_path)


if __name__ == '__main__':
    main()
