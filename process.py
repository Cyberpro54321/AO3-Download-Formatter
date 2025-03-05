#!/bin/python3

import argparse  # https://docs.python.org/3/library/argparse.html
import configparser  # https://docs.python.org/3/library/configparser.html
import csv  # https://docs.python.org/3/library/csv.html
import os.path  # https://docs.python.org/3/library/os.path.html
import datetime  # https://docs.python.org/3/library/datetime.html

version = "0.3 rc1"
startTime = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()

# argparse
parser = argparse.ArgumentParser()
parser.add_argument("rawName")
parser.add_argument("-c", "--config", default="config/config.ini")
parser.add_argument("-d", "--database", default="config/db.csv")
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
if config["ao3css"].getboolean("merged"):
    stylesheets = [
        ["screen", "1_site_screen_.css"],
        ["only screen and (max-width: 62em), handheld", "4_site_midsize.handheld_.css"],
        ["only screen and (max-width: 42em), handheld", "5_site_narrow.handheld_.css"],
        ["speech", "6_site_speech_.css"],
        ["print", "7_site_print_.css"],
    ]
else:
    stylesheets = [
        ["screen", "01-core.css"],
        ["screen", "02-elements.css"],
        ["screen", "03-region-header.css"],
        ["screen", "04-region-dashboard.css"],
        ["screen", "05-region-main.css"],
        ["screen", "06-region-footer.css"],
        ["screen", "07-interactions.css"],
        ["screen", "08-actions.css"],
        ["screen", "09-roles-states.css"],
        ["screen", "10-types-groups.css"],
        ["screen", "11-group-listbox.css"],
        ["screen", "12-group-meta.css"],
        ["screen", "13-group-blurb.css"],
        ["screen", "14-group-preface.css"],
        ["screen", "15-group-comments.css"],
        ["screen", "16-zone-system.css"],
        ["screen", "17-zone-home.css"],
        ["screen", "18-zone-searchbrowse.css"],
        ["screen", "19-zone-tags.css"],
        ["screen", "20-zone-translation.css"],
        ["screen", "21-userstuff.css"],
        ["screen", "22-system-messages.css"],
        ["only screen and (max-width: 62em), handheld", "25-media-midsize.css"],
        ["only screen and (max-width: 42em), handheld", "26-media-narrow.css"],
        ["speech", "27-media-aural.css"],
        ["print", "28-media-print.css"],
    ]


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
reasonableMaxHeadLength = 200
workID = ""
styleBuiltinStart = 0
styleBuiltinEnd = 0
with open(rawFullName, "r") as raw:
    for i in raw:
        j = i.strip()
        if j != "":
            bufferMain.append(j)
for i in range(reasonableMaxHeadLength):
    if bufferMain[i].find("archiveofourown.org/works/") != -1 and not workID:
        temp = bufferMain[i].find("archiveofourown.org/works/") + len(
            "archiveofourown.org/works/"
        )
        workID = bufferMain[i][temp: temp + 8]
        del temp
        print("Work ID:   " + workID)
    if (not styleBuiltinStart) and bufferMain[i].find("<style") != -1:
        styleBuiltinStart = i
    if (not styleBuiltinEnd) and bufferMain[i].find("</style>") != -1:
        styleBuiltinEnd = i
for i in range(styleBuiltinStart, styleBuiltinEnd + 1):
    bufferMain.pop(styleBuiltinStart)
del styleBuiltinStart
del styleBuiltinEnd

headEnd = 0
for i in range(reasonableMaxHeadLength):
    if (not headEnd) and bufferMain[i].find("</head>") != -1:
        headEnd = i
for i in reversed(stylesheets):
    bufferMain.insert(
        headEnd,
        '<link rel="stylesheet" type="text/css" media="'
        + i[0]
        + '" href="'
        + dirAO3CSS
        + "/"
        + i[1]
        + '">',
    )
del headEnd

bodyStart = 0
for i in range(reasonableMaxHeadLength):
    if (not bodyStart) and bufferMain[i].find("<body") != -1:
        bodyStart = i
bufferMain.insert(bodyStart + 1, '<div class="wrapper">')
bufferMain.insert(bodyStart + 1, '<div id="main" class="works-show-region">')
bufferMain.insert(bodyStart + 1, '<div id="inner" class="wrapper">')
bufferMain.insert(bodyStart + 1, '<div id="outer" class="wrapper">')
bodyEnd = 0
for i in range(len(bufferMain) - 50, len(bufferMain)):
    if (not bodyEnd) and bufferMain[i].find("</body>") != -1:
        bodyEnd = i
for i in range(4):
    bufferMain.insert(bodyEnd, "</div>")
del bodyEnd

bufferMain.remove('<div id="preface">')
bufferMain[bufferMain.index('<dl class="tags">')] = '<dl class="work meta group">'
bufferMain[bufferMain.index('<div id="afterword">')] = (
    '<div class="afterword preface group">'
)
bufferMain.pop(bufferMain.index('<div id="chapters" class="userstuff">') - 1)

workName = ""
for i in range(reasonableMaxHeadLength):
    if (not workName) and bufferMain[i].find("<h1>") != -1:
        workName = bufferMain[i][
            bufferMain[i].find(">") + 1: bufferMain[i].find("<", 3)
        ]
        print("Work Name: " + workName)
        bufferMain.insert(i, '<div class="preface group">')
        bufferMain.insert(i, '<div id="workskin">')
        bufferMain.insert(i, "</div>")
        bufferMain.insert(i, "</div>")

chapterLine = ""
chapterCountMax = ""
chapterCountCurrent = 0
for i in range(reasonableMaxHeadLength):
    if (not chapterLine) and bufferMain[i].find("Chapters: ") != -1:
        chapterLine = bufferMain[i]
chapterCountCurrent = int(chapterLine.split()[1].split("/")[0])
chapterCountMax = chapterLine.split()[1].split("/")[1]
print("Chapter #: " + str(chapterCountCurrent) + "/" + chapterCountMax)

bufferMain.append(
    "<!-- This file written by AO3 Download Formatter version "
    + version
    + " at "
    + startTime
    + "-->"
)


fieldnames = [
    "Work Name",
    "Work ID",
    "Current Chapter Count",
    "Current Total Chapter Count",
    "Date Formatted",
]
db = []
if os.path.exists(args.database):
    with open(args.database, "r") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            if row[fieldnames[1]] != fieldnames[1]:
                db.append(row)
else:
    print("No existing database detected, creating new one...")
alreadyInDB = False
for i in db:
    if i[fieldnames[1]] == workID:
        i[fieldnames[0]] = workName.strip(",")
        i[fieldnames[2]] = chapterCountCurrent
        i[fieldnames[3]] = chapterCountMax
        i[fieldnames[4]] = startTime
        alreadyInDB = True
if not alreadyInDB:
    db.append(
        {
            fieldnames[0]: workName.strip(","),
            fieldnames[1]: workID,
            fieldnames[2]: chapterCountCurrent,
            fieldnames[3]: chapterCountMax,
            fieldnames[4]: startTime,
        }
    )
with open(args.database, "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in db:
        writer.writerow(i)


outputNameCoreMaxLength = 255 - len("_[]") - len(workID) - len(".html")
outputName = ""
for i in workName:
    if i.isascii() and i.isprintable():
        outputName = outputName + i
outputName = outputName.strip('/<>:"\\|?*')
if len(outputName) > outputNameCoreMaxLength:
    outputName = outputName[:outputNameCoreMaxLength]
outputName = outputName + " [" + workID + "]" + ".html"
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
print("Saved formatted file to " + outputFullName)
