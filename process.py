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
rawFullName = dirStorageProcessed + dirRaws + "/" + rawName
if not os.path.exists(rawFullName):
    raise Exception("File not found: " + rawFullName)
bufferMain = []
workID = ""
workName = ""
with open(rawFullName, "r") as raw:
    for i in raw:
        j = i.strip()
        if j != "":
            bufferMain.append(j)
for i in range(len(bufferMain)):
    if bufferMain[i].find("<h1>") != -1 and not workName:
        workName = bufferMain[i][
            bufferMain[i].find(">") + 1: bufferMain[i].find("<", 3)
        ]
        print(workName)
    if bufferMain[i].find("archiveofourown.org/works/") != -1 and not workID:
        temp = bufferMain[i].find("archiveofourown.org/works/") + len(
            "archiveofourown.org/works/"
        )
        workID = bufferMain[i][temp: temp + 8]
        del temp
        print(workID)
    if bufferMain[i].find("<style") != -1:
        styleBuiltinStart = i
    if bufferMain[i].find("</style>") != -1:
        styleBuiltinEnd = i
for i in range(styleBuiltinStart, styleBuiltinEnd + 1):
    bufferMain.pop(styleBuiltinStart)

outputNameCoreMaxLength = 255 - len("_[]") - len(workID) - len(".html")
outputName = workName.replace(" ", "_")
outputName = outputName.strip("/\\!#$%^*|;:<>?")
if len(outputName) > outputNameCoreMaxLength:
    outputName = outputName[:outputNameCoreMaxLength]
outputName = outputName + "_[" + workID + "]" + ".html"
outputFullName = dirStorageProcessed + dirOutput + "/" + outputName
with open(outputFullName, "w") as output:
    indent = 0
    for i in bufferMain:
        if (i.find("<div") == -1 and i.find("</div>") != -1) or (
            i.find("<head") == -1 and i.find("</head>") != -1
        ):
            indent -= 1
        outputString = ""
        for j in range(indent):
            outputString = outputString + "  "
        outputString = outputString + i + "\n"
        output.write(outputString)
        if (i.find("<div") != -1 and i.find("</div>") == -1) or (
            i.find("<head") != -1 and i.find("</head>") == -1
        ):
            indent += 1
