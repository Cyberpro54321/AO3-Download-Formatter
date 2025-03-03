#!/bin/python3

import argparse  # https://docs.python.org/3/library/argparse.html
import configparser  # https://docs.python.org/3/library/configparser.html
import csv  # https://docs.python.org/3/library/csv.html
import os.path  # https://docs.python.org/3/library/os.path.html

# argparse
parser = argparse.ArgumentParser()
parser.add_argument("rawName")
parser.add_argument("-c", "--config", default="config/config.ini")
args = parser.parse_args()

# configparser
config = configparser.ConfigParser()
config.read(args.config)

# parseparser
rawName = args.rawName
if rawName[-5:] != ".html":
    rawName = rawName + ".html"
dirStorageRaw = config["dir"]["storage"]
dirStorageProcessed = os.path.abspath(os.path.expanduser(dirStorageRaw))
if dirStorageProcessed[-1:] != "/":
    dirStorageProcessed = dirStorageProcessed + "/"
dirRaws = config["dir"]["raws"]
dirOutput = config["dir"]["output"]
dirWorkskins = config["dir"]["workskins"]
if config["ao3css"]["in_storage"]:
    dirAO3CSS = dirStorageProcessed + config["dir"]["ao3css"]
else:
    dirAO3CSS = config["dir"]["ao3css"]


# main
for i in [
    dirStorageProcessed,
    dirStorageProcessed + dirRaws,
    dirStorageProcessed + dirOutput,
    dirStorageProcessed + dirWorkskins,
    dirAO3CSS,
]:
    if not os.path.exists(i):
        raise Exception(
            "Directory referenced by config file ("
            + args.config
            + ") doesn't exist: "
            + i
        )
print("Searching for " + rawName + " in " + dirStorageProcessed + dirRaws)
