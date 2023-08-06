from sys import argv, exit

from list.cli import Processor


def main():
    args = argv[1:]
    processor = Processor(*args)
    result = processor.process()
    exit(0 if result else 1)


if __name__ == '__main__':
    main()
