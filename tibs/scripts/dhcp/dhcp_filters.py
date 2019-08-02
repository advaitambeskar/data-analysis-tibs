import numpy as np
import pandas as pd
import re

"""
Contains some common filters for getting data from the dhcp file
"""
class DHCPFilters:    

    @staticmethod
    def filter_time_range(traces, start_time, end_time):
        """
        Filters out all times not within the provided start time and duration

        The ranges are inclusive.

        :parameters:
            dhcp_file (pandas dataframe): the dhcp data frame to filter
            start_time (int): starting epoch time
            duration (int): duration of the filter time
        :return:
            pandas dataframe with times only between the start time and duration
        """
        traces = traces.loc[traces['startTime'] >= start_time]
        traces = traces.loc[traces['startTime'] <= end_time]
        return traces

    @staticmethod
    def filter_time(traces, start_time, duration):
        """
        Filters out all times not within the provided start time and duration

        The ranges are inclusive.

        :parameters:
            dhcp_file (pandas dataframe): the dhcp data frame to filter
            start_time (int): starting epoch time
            duration (int): duration of the filter time
        :return:
            pandas dataframe with times only between the start time and duration
        """
        traces = traces.loc[traces['startTime'] >= start_time]
        traces = traces.loc[traces['endTime'] <= start_time + duration]
        return traces
        
    @staticmethod
    def filter_user(traces, user_id):
        """
        Filters out all traces that do not belong to the specific user id

        :parameters:
            dhcp_file (pandas dataframe): the dhcp data frame to filter
            user_id (int): the id of the user
        :return:
            pandas dataframe with traces belonging to the user
        """
        user_traces = traces.loc[traces['userMAC'] == user_id]
        return user_traces
        
    @staticmethod
    def filter_users(traces, user_ids):
        """
        Filters out all traces that do not belong to list of users

        :parameters:
            dhcp_file (pandas dataframe): the dhcp data frame to filter
            user_ids (list): the list of user ids
        :return:
            pandas dataframe with traces belonging to the user
        """
        return traces.loc[user_ids.contains(traces['userMAC'])]
    
    @staticmethod
    def filter_building(traces, locations, building_name):
        """
        Filters out all traces that do not visit the specified building

        :parameters:
            traces(pandas dataframe): the dhcp data frame to filter
            locations(pandas dataframe): the locations data
            building_name (str): the name of the building
        :returns:
            pandas dataframe with traces for the specific location
        """
        # TODO
        return traces
    
    @staticmethod
    def write_building_names(dhcp_file, location_file, file_name):
        """
        Writes the visited building next to the event
        """
        traces = pd.read_csv(dhcp_file)
        locations = pd.read_csv(location_file)

        buildings = []
        for index, row in traces.iterrows():
            prefix = re.findall('[a-zA-Z]+', row['APNAME'])[0]
            building = locations.loc[locations['prefix'] == prefix]
            if (building.size == 0):
                building_name = 'unknown'
            else:
                building_name = building['name'].values[0]
            buildings.append(building_name)
        traces['building'] = buildings
        traces.to_csv(file_name, index=None)
    
    @staticmethod
    def write_traces_building_names(traces, location_file, file_name):
        """
        Writes the visited building next to the event
        """
        locations_data = pd.read_csv(location_file)
        locations = {}
        for index, row in locations_data.iterrows():
            locations[row['prefix']] = row
        locations['unknown'] = np.array([])

        buildings = []
        for index, row in traces.iterrows():
            prefix = re.findall('[a-zA-Z]+', row['APNAME'])[0]
            try:
                building = locations[prefix]
                if (building.size == 0):
                    building_name = 'unknown'
                else:
                    building_name = building['name']
            except:
                building_name = 'unknown'
            buildings.append(building_name)
        traces['building'] = buildings
        traces.to_csv(file_name, index=None)