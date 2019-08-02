import numpy as np
import pandas as pd

class LocationWriter:
    def __init__(self, location_file):
        self.location_file = location_file
        self.locations = pd.read_csv(location_file)
    
    def get_building_dictionary(self):
        building_in_trip = {}
        for building in self.locations['name']:
            building_in_trip[building] = 0
        return building_in_trip

    def add_column(self, column_name, dictionary):
        column = []
        for building in self.locations['name']:
            column.append(dictionary[building])
        self.locations[column_name] = column

    def write_file(self, file_name):
        replace_file_name = "r{0}".format(file_name)
        self.locations.to_csv(replace_file_name, index=None)