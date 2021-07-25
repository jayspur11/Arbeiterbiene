import csv
import data

from importlib.resources import open_text

geocodes = {}
with open_text(data, "uszips.csv") as geocodes_infile:
    reader = csv.DictReader(geocodes_infile)
    for row in reader:
        geocodes[row["zip"]] = row
