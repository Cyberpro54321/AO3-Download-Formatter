#!/bin/python3

import argparse  # https://docs.python.org/3/library/argparse.html
import configparser  # https://docs.python.org/3/library/configparser.html
import csv  # https://docs.python.org/3/library/csv.html
import os.path  # https://docs.python.org/3/library/os.path.html
import datetime  # https://docs.python.org/3/library/datetime.html

version = "0.8.0"
startTime = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()


def dirParser(input: str):
    input = os.path.abspath(os.path.expanduser(input))
    if input[-1:] != "/":
        return input + "/"
    else:
        return input


# argparse
parser = argparse.ArgumentParser()
parser.add_argument("rawName")
parser.add_argument("-c", "--config", default="config/config.ini")
parser.add_argument("-d", "--database", default="config/db.csv")
parser.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("-s", "--silent", action="store_true")
parser.add_mutually_exclusive_group()
parser.add_argument("--no-database", action="store_true")
parser.add_argument("--yes-database", action="store_true")
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
useDB = config["csv"].getboolean("use")
if args.no_database:
    useDB = False
if args.yes_database:
    useDB = True
dbLocation = config["csv"]["file"]
if args.database != "config/db.csv":
    dbLocation = args.database
rawName = args.rawName
if rawName[-5:] != ".html":
    rawName = rawName + ".html"
dirRaws = dirParser(config["dir"]["raws"])
dirOutput = dirParser(config["dir"]["output"])
dirWorkskins = dirParser(config["dir"]["workskins"])
dirAO3CSS = dirParser(config["dir"]["ao3css"])
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
    dirRaws,
    dirOutput,
    dirWorkskins,
    dirAO3CSS,
]:
    if not os.path.exists(i):
        raise Exception(
            "Directory referenced by config file ("
            + args.config
            + ") doesn't exist: "
            + i
        )
if (not args.quiet) and (not args.silent):
    print("Searching for " + rawName + " in " + dirRaws)
rawFullName = dirRaws + rawName
if not os.path.exists(rawFullName):
    raise Exception("File not found: " + rawFullName)
bufferMain = []
workID = ""
styleBuiltinStart = 0
styleBuiltinEnd = 0
with open(rawFullName, "r") as raw:
    for i in raw:
        j = i.strip()
        if j != "":
            bufferMain.append(j)
reasonableMaxHeadLength = 350
if len(bufferMain) < reasonableMaxHeadLength:
    reasonableMaxHeadLength = len(bufferMain)
for i in range(reasonableMaxHeadLength):
    if (not workID) and bufferMain[i].find("archiveofourown.org/works/") != -1:
        temp = bufferMain[i].find("archiveofourown.org/works/") + len(
            "archiveofourown.org/works/"
        )
        workID = bufferMain[i][temp: bufferMain[i].find('"', temp, temp + 10)]
        del temp
        if (not args.quiet) and (not args.silent):
            print("Work ID:   " + workID)
    if (not styleBuiltinStart) and bufferMain[i].find("<style") != -1:
        styleBuiltinStart = i
    if (not styleBuiltinEnd) and bufferMain[i].find("</style>") != -1:
        styleBuiltinEnd = i
for i in range(styleBuiltinStart, styleBuiltinEnd + 1):
    bufferMain.pop(styleBuiltinStart)
del styleBuiltinStart
del styleBuiltinEnd


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
        if (not args.quiet) and (not args.silent):
            print("Work Name: " + workName)
        bufferMain.insert(i, '<div class="preface group">')
        bufferMain.insert(i, '<div id="workskin">')
        bufferMain.insert(i, "</div>")
        bufferMain.insert(i, "</div>")

outputNameCoreMaxLength = 255 - len("_[]") - len(workID) - len(".html")
outputNameCore = ""
for i in workName:
    if i.isascii() and i.isprintable():
        outputNameCore = outputNameCore + i
outputNameCore = outputNameCore.replace('"', "'")
outputNameCore = outputNameCore.strip("/<>:\\|?*")
if len(outputNameCore) > outputNameCoreMaxLength:
    outputNameCore = outputNameCore[:outputNameCoreMaxLength]
outputNameCore = outputNameCore + " [" + workID + "]"
outputFullName = dirOutput + outputNameCore + ".html"


headEnd = 0
for i in range(reasonableMaxHeadLength):
    if (not headEnd) and bufferMain[i].find("</head>") != -1:
        headEnd = i
bufferMain.insert(
    headEnd,
    '<link rel="stylesheet" href="' + dirWorkskins + outputNameCore + '.css">',
)
bufferMain.insert(
    headEnd, '<link rel="stylesheet" href="' + dirAO3CSS + 'sandbox.css">'
)
for i in reversed(stylesheets):
    bufferMain.insert(
        headEnd,
        '<link rel="stylesheet" type="text/css" media="'
        + i[0]
        + '" href="'
        + dirAO3CSS
        + i[1]
        + '">',
    )
del headEnd
chapterLine = ""
chapterCountMax = ""
chapterCountCurrent = 0
chapterIndex = 0
while not chapterLine:
    if bufferMain[chapterIndex].find("Chapters:") != -1:
        chapterLine = bufferMain[chapterIndex]
    chapterIndex += 1
chapterCountCurrent = int(chapterLine.split()[1].split("/")[0])
chapterCountMax = chapterLine.split()[1].split("/")[1]
if (not args.quiet) and (not args.silent):
    print("Chapter #: " + str(chapterCountCurrent) + "/" + chapterCountMax)

bufferMain.append(
    "<!-- This file written by AO3 Download Formatter version "
    + version
    + " at "
    + startTime
    + "-->"
)


if useDB:
    fieldnames = [
        "Work ID",
        "Work Name",
        "Current Chapter Count",
        "Current Total Chapter Count",
        "Date Formatted",
    ]
    db = []
    if os.path.exists(dbLocation):
        with open(dbLocation, "r") as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            for row in reader:
                if row[fieldnames[0]] != fieldnames[0]:
                    db.append(row)
    else:
        if not args.silent:
            print("No existing database detected, creating new one...")
    alreadyInDB = False
    for i in db:
        if i[fieldnames[0]] == workID:
            i[fieldnames[1]] = outputNameCore
            i[fieldnames[2]] = chapterCountCurrent
            i[fieldnames[3]] = chapterCountMax
            i[fieldnames[4]] = startTime
            alreadyInDB = True
    if not alreadyInDB:
        db.append(
            {
                fieldnames[0]: workID,
                fieldnames[1]: workName.strip(","),
                fieldnames[2]: chapterCountCurrent,
                fieldnames[3]: chapterCountMax,
                fieldnames[4]: startTime,
            }
        )
    with open(dbLocation, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for i in db:
            writer.writerow(i)


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
if (not args.quiet) and (not args.silent):
    print("Saved formatted file to " + outputFullName)
