# AO3 Download Formatter
A script for reformatting [AO3](https://archiveofourown.org)'s official HTML downloads into something closer to reading on the official website

## Setup
1. Download this repository.
2. Make a copy of `config.default.ini` in the `config` folder, named `config.ini`, then change the settings as you like.
```bash
cp config.default.ini config/config.ini
editor config/config.ini
```
3. Make sure the directories referenced in `config.ini` exist, and that the user you'll be running the scripts as has write permissions for the Output folder and at least read permissions for the Raws folder.

## Usage
### Basic Usage
```bash
./process.py <name>
```
Where `<name>` is the name of the raw HTML file you want to format.
So with the default settings, the file `~/Documents/AO3/Raws/Mortified.html` can be formatted with:
```bash
./process.py Mortified
```
or
```bash
./process.py Mortified.html
```

### Arguments for process.py
- `--config` (or `-c`) allows you to specify a location for your config file other than `config/config.ini`.
- `--database` (or `-d`) allows you to specify a location for `db.csv` (described below). The default location is `config/db.csv`.
- `--quiet` (or `-q`) limits the messages that get printed to your screen to just the irregular ones not expected to be triggered every usage.
- `--silent` (or `-s`) prevents any messages from getting printed to your screen except for fatal error messages.
- `--no-database` disables the use of `db.csv`
- `--yes-database` re-enables the use of `db.csv` if it was disabled in the config file.

### bulk-processer.py
`bulk-processer.py` will attempt to run all files in your 'Raws' directory through `process.py`. It also accepts the `--config` and `--quiet` arguments, which do the same as for `process.py`, and `--database`, though `bulk-processer.py` doesn't actually use the database file and this is just passed through to `process.py` unchanged.

## Configuration
### dir
- `raws`: The folder containing your 'raw' HTML files (the ones downloaded directly from AO3).
- `workskins`: The folder containing .css files corresponding to each work's workskin.
- `output`: The folder the files produced by `process.py` will be written to.
- `ao3css`: The folder containing the official .css files served by the AO3 website.

### ao3css
- `merged`: If you downloaded 5 .css file from AO3, starting with `1_site_screen_.css` and ending with `7_site_print_.css`, set this to True. If you downloaded 26 .css file from AO3, starting with `01-core.css` and ending with `28-media-print.css`, set this to False. If you know why AO3 sometimes serves 5 css files and sometimes serves 26, contact me.

### csv
If allowed to, this project will record the names, ID numbers, and chapter counts of every work you format with it, as well as a timestamp recording when you did so. This is intended to eventually be used with another script that will semi-automatically download and format new chapters when they're released, but that script doesn't exist yet.
All the options in this section can be overridden by the `--database`, `--no-database`, and `--yes-database` arguments at runtime.
- `file`: The file to be used.
- `use`: True or false whether to use it or not.
