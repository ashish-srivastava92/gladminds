import csv
import os
import sys

BASE_DIR = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
sys.path.append(BASE_DIR)

class CSVParser():

    def __init__(self, location):
        '''
            Location should be start from project base directory
        '''
        self.location = location

    def get_csv_parse_obj(self, file_name, location=None):
        if location:
            self.location = location

        with open(file_name, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                print ', '.join(row)
        return spamreader


##########################################################################
###########################General Parser###################################
csv_parser = CSVParser(BASE_DIR)
location = os.path.join(BASE_DIR, 'python-csv-parser')
file_name = "UCN_VIN_DATA_WITH_ERRORS.csv"
csv_parser.get_csv_parse_obj(file_name, location)

## Define Logic for CSV Parser Here##
##########################################################################