#!/bin/python3

import os  # https://docs.python.org/3/library/os.html
import subprocess  # https://docs.python.org/3/library/subprocess.html
import os.path  # https://docs.python.org/3/library/os.path.html
import configparser  # https://docs.python.org/3/library/configparser.html
import argparse  # https://docs.python.org/3/library/argparse.html


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", default="config/config.ini")
parser.add_argument("-d", "--database", default="config/db.csv")
parser.add_argument("-q", "--quiet", action="store_true")
args = parser.parse_args()
if not os.path.exists(args.config):
    if args.config == "config/config.ini":
        with open("config.default.ini", "r") as default:
            with open("config/config.ini", "w") as target:
                for i in default:
                    target.write(i)
    else:
        raise Exception("Config file '" + args.config + "' doesn't exist.")
config = configparser.ConfigParser()
config.read(args.config)

dirStorage = os.path.abspath(os.path.expanduser(config["dir"]["storage"]))
if dirStorage[-1:] != "/":
    dirStorage = dirStorage + "/"
dirRawsFull = dirStorage + config["dir"]["raws"]

allRaws = os.listdir(dirRawsFull)
for work in allRaws:
    if not args.quiet:
        print("Now formatting: " + work)
    subprocess.run(["./process.py", "-c", args.config, "-d", args.database, "-q", work])
