#!/bin/python3

import argparse  # https://docs.python.org/3/library/argparse.html
import configparser  # https://docs.python.org/3/library/configparser.html
import csv  # https://docs.python.org/3/library/csv.html

parser = argparse.ArgumentParser()
parser.add_argument("rawName")
args = parser.parse_args()

print(args.rawName)
