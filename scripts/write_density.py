# -*- coding: utf-8 -*-
import calendar
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import ntpath
import math
import operator
import pandas as pd
import pytz
import re

# TODO add method to get the visited buildings and total time that a user visits the buildings
# TODO add method to get the visited categories and total time that a user visits the categories
class DHCPAnalysis:
    def __init__(self, dhcp_file, location_file):
        self.file = dhcp_file
        self.location_file = location_file
        
        self.traces = pd.read_csv(dhcp_file)
        self.locations = pd.read_csv(location_file)
        
        # Convert epoch times to pandas date time
        self.traces['startTime'] = pd.DatetimeIndex(pd.to_datetime(self.traces['startTime'], unit='s')).tz_localize('UTC')
        self.traces['endTime'] = pd.DatetimeIndex(pd.to_datetime(self.traces['endTime'], unit='s')).tz_localize('UTC')
                
        # Get the earliest and latest times
        self.earliest_time = min(self.traces['startTime'].min(), self.traces['endTime'].min())
        self.latest_time = max(self.traces['startTime'].max(), self.traces['endTime'].max())
        
        # Get the first and last user index
        self.first_user_id = self.traces['userMAC'].min()
        self.last_user_id = self.traces['userMAC'].max()
                
        # Get the date from the file name
        fileName = ntpath.basename(self.file)
        date_string = re.findall('[0-9]{8}', fileName)[0]
        self.date = dt.datetime.strptime(date_string, '%Y%m%d')
                
    def calculate_events_per_building(self):
        """
        Calculates the number of events that occur at a building
        """
        buildings = self.locations['name'].values
        building_events = {}
        for building in buildings:
            building_events[building] = 0
        building_events['unknown'] = 0
        
        for index, row in self.traces.iterrows():
            prefix = re.findall('[a-zA-Z]+', row['APNAME'])[0]
            building = self.locations.loc[self.locations['prefix'] == prefix]
            if (building.size == 0):
                building = 'unknown'
            else:
                building = building['name'].values[0]
            building_events[building] += 1
        return building_events
    
    def calculate_unique_events_per_building(self):
        """
        Calculates the number of unique device IDs that visit a building
        """
        buildings = self.locations['name'].values
        building_count = {}
        for building in buildings:
            building_count[building] = 0
        building_count['unknown'] = 0
        
        for user_index in range(self.first_user_id, self.last_user_id):
            visited_buildings = self.get_visited_buildings(user_index)
            for visited_building in visited_buildings:
                building_count[visited_building] += 1
        return building_count
    
    def get_traces_of_user(self, user_id):
        """
        Gets all traces of the user
        """
        return self.traces[self.traces['userMAC'] == user_id]
    
    def get_building_from_ap(self, access_point):
        """
        Gets the building name from the access point name
        """
        building = ""
        if access_point == 'unknown':
            building = 'unknown'
        else:
            prefix = re.findall('[a-zA-Z]+', access_point)[0]
            building = self.locations.loc[self.locations['prefix'] == prefix]
            if (building.size == 0):
                building = 'unknown'
            else:
                building = building['name'].values[0]
        return building;
    
    def get_visited_buildings(self, user_id):
        """
        Gets all buildings visited by the user
        """
        user_traces = self.get_traces_of_user(user_id)
        access_points = user_traces['APNAME'].unique()
        unique_buildings = set()
        for access_point in access_points:
            building = analysis.get_building_from_ap(access_point)
            unique_buildings.add(building)
        return unique_buildings
    
    def write_building_csv(self, path):
        """
        Writes a csv file with the 
        """
        ext_locations = self.locations;
        unique_building_events = analysis.calculate_unique_events_per_building()
        ext_locations['unique'] = self.locations['name'].map(unique_building_events)
        ext_locations.to_csv(path)
        
        building_events = analysis.calculate_events_per_building()
        ext_locations['total'] = self.locations['name'].map(building_events)
        ext_locations.to_csv(path)
    
if __name__ == "__main__":
    style_file = '../data/style/tibs_plot_style.mplstyle'
    data_file = '../../data/outputwireless-logs-20120407.DHCP_ANON.csv'
#    data_file = '../data/outputwireless-logs-20120409.DHCP_ANON.csv'
    location_file = '../../data/prefix_lat_lon_name_category.csv'
    
    output_location_file = '../../data/density_locations_20120407.csv'
    
    if (ntpath.isfile(style_file)):
        plt.style.use(style_file)
#    
    if (ntpath.isfile(data_file) and ntpath.isfile(location_file)):
        analysis = DHCPAnalysis(data_file, location_file)
        analysis.write_building_csv(output_location_file)
        
#        building_count = analysis.calculate_events_per_building()
#        fig, ax = plt.subplots()
#        max_value = np.amax(building_count)
#        plt.bar(range(len(building_count)), list(building_count.values()), align='edge', width=1)
#        plt.xticks(range(len(building_count)), list(building_count.keys()), rotation=90)
#        ax.set_ylim([0, max(building_count.values()) * 1.15])
#        plt.gcf().subplots_adjust(bottom=0.4)
#        plt.show()
    else:
        print('Error: File {0} does not exist'.format(data_file))
    