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
- `--database` (or `-d`) allows you to specify a location for a .csv file that tracks the name, ID number, and chapter counts of all the works you format with this tool. The default location is `config/db.csv`, and there is currently no way to prevent the file from being written.
- `--quiet` (or `-q`) limits the messages that get printed to your screen to just the irregular ones not expected to be triggered every usage.
- `--silent` (or `-s`) prevents any messages from getting printed to your screen except for fatal error messages.

### bulk-processer.py
`bulk-processer.py` will attempt to run all files in your 'Raws' directory through `process.py`. It also accepts the `--config` and `--quiet` arguments, which do the same as for `process.py`, and `--database`, though `bulk-processer.py` doesn't actually use the database file and this is just passed through to `process.py` unchanged.
