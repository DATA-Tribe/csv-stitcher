# Importing the relevant libraries
import csv
import sys
import getopt

from datetime import datetime
from os import listdir
from os.path import isfile, join


# Rewriting the list comprehension from above
"""
files = []
for file in listdir(path):
    if isfile(join(path, file)):
        files.append(file)
"""

# Creating a list with the file's header
headers = [
    '#',
    'Keyword',
    'Position',
    'Position History',
    'Position History Date',
    'Volume',
    'URL',
    'Difficulty',
    'Traffic (desc)',
    'CPC',
    'Last Update',
    'Page URL inside',
    'SERP Features',
    'Domain',
    'Country Code',
    'Date Created',
]


def main(argv):
    # Declaring the path to the folder containing all the files
    path = "kwfiles/"

    # Declaring new variable which will contain the merged file from user input
    output_file = "new-merged-file.csv"

    # Checks that arguments have been passed in
    if not argv:
        print("-i <input file path> -o <output csv file> parameters must be specified")
        print("Example: python3 stitcher.py -i kwfiles -o test-file.csv")
        sys.exit(1)

    # Catches any errors if the arguments passed in are not valid
    try:
        opts, args = getopt.getopt(argv, "i:o:", ["path=", "out-file="])
    except getopt.GetoptError:
        print("stitcher.py -i <input file path> -o <output csv file>")
        print("Example: python3 stitcher.py -i kwfiles -o test-file.csv")
        sys.exit(1)

    # Looping through all optional arguments passed in checking each and setting path and output file
    for opt, arg in opts:
        if opt in ("-i", "--path"):
            # sets the path from arg parameter with correct trailing slash
            path = arg + "/"
        if opt in ("-o", "--out-file"):
            # Creating a file writer. This will allow us to write in our newly created csv
            output_file = open(arg, 'w', newline='\n')

    # Creating a new list of file names with a loop that checks for files, eliminating folders
    files = [f for f in listdir(path) if isfile(join(path, f))]

    # Declaring the variable writer where we input our file name and the headers declared above as arguments
    writer = csv.DictWriter(output_file, fieldnames=headers)

    # The actual writing of the headers
    writer.writeheader()

    # Looping through the list of file names declared above
    for file in files:
        # Extracting the domain name
        domain = file.split('-organic')[0]
        # Extracting the country code
        country_code = file.split('subdomains-')[1][:2]
        # Extracting and formatting the date
        date_string = file.split('_')[0][-11:]
        date_obj = datetime.strptime(date_string, "%d-%b-%Y")
        date_formatted = date_obj.strftime("%d/%m/%Y")

        # Opening the csv_files one at a time and reading its content, specifying its delimiter
        with open(path + file, mode='r', encoding='utf-16') as csv_file:
            reader = csv.DictReader(csv_file, delimiter="\t")

            # Using the writer, we are writing the new 3 columns to the file
            for row in reader:
                row["Domain"] = domain
                row["Country Code"] = country_code
                row["Date Created"] = date_formatted
                writer.writerow(row)

    output_file.close()


if __name__ == "__main__":
    main(argv=sys.argv[1:])
