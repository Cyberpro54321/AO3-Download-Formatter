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
dirStorageRaw = config["General"]["dir_storage"]
dirStorageProcessed = os.path.abspath(os.path.expanduser(dirStorageRaw))
if dirStorageProcessed[-1:] != "/":
    dirStorageProcessed = dirStorageProcessed + "/"
dirRaws = config["General"]["dir_raws"]
dirOutput = config["General"]["dir_output"]
dirWorkskins = config["General"]["dir_workskins"]
if config["General"]["ao3css_in_storage"]:
    dirAO3CSS = dirStorageProcessed + config["General"]["dir_ao3css"]
else:
    dirAO3CSS = config["General"]["dir_ao3css"]


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
if not os.path.exists(dirStorageProcessed):
    print(dirStorageProcessed + " doesn't seem to exist.")
print("Searching for " + rawName + " in " + dirStorageProcessed + dirRaws)
