import argparse
from preprocessor import processor


def compile(args: argparse.Namespace):
    processor.process(args)
    pass