from .hub import Hub

import pandas as pd

class Hubs:
    def __init__(self, location_file):
        self.location_file = location_file
        self.locations = pd.read_csv(self.location_file)

        self.hubs = []
        for index, row in self.locations.iterrows():
            building_name = row['name']
            lat = row['lat']
            lon = row['lon']
            cap = row['cap']
            hub = Hub(row, building_name, lat, lon, cap)
            self.hubs.append(hub)
    
    def determine_routes(self, start_lat, start_lon, stop_lat, stop_lon, hour):
        start_hubs = self.get_closest_hubs(start_lat, start_lon)
        stop_hubs = self.get_closest_hubs(stop_lat, stop_lon)

        start_incentives = []
        for start_hub in start_hubs:
            if (start_hub['dist'] <= 0.1):
                in_str = 'in_h{0}'.format(hour)
                out_str = 'out_h{0}'.format(hour)

                start_hub_name = start_hub['hub'].name
                hub = self.locations.loc[self.locations['name'] == start_hub_name].head(1)

                in_trips = hub[in_str].values[0]
                out_trips = hub[out_str].values[0]
                trip_difference = in_trips - out_trips
                num_trips = start_hub['hub'].availability + trip_difference
                start_hub['hub'].set_availability(num_trips)
                incentive = start_hub['hub'].surplus_incentive(start_lat, start_lon)
                hub_with_inc = {}
                hub_with_inc['hub'] = start_hub['hub']
                hub_with_inc['award'] = incentive
                hub_with_inc['distance'] = start_hub['dist']
                start_incentives.append(hub_with_inc)

        stop_incentives = []
        for stop_hub in stop_hubs:
            if (stop_hub['dist'] <= 0.1):
                in_str = 'in_h{0}'.format(hour)
                out_str = 'out_h{0}'.format(hour)

                stop_hub_name = stop_hub['hub'].name
                hub = self.locations.loc[self.locations['name'] == stop_hub_name].head(1)

                in_trips = hub[in_str].values[0]
                out_trips = hub[out_str].values[0]
                trip_difference = in_trips - out_trips
                num_trips = stop_hub['hub'].availability + trip_difference
                stop_hub['hub'].set_availability(num_trips)
                incentive = stop_hub['hub'].surplus_incentive(stop_lat, stop_lon)
                hub_with_inc = {}
                hub_with_inc['hub'] = stop_hub['hub']
                hub_with_inc['award'] = incentive
                hub_with_inc['distance'] = stop_hub['dist']
                stop_incentives.append(hub_with_inc)
        
        start_incentives = sorted(start_incentives, key=lambda k: k['award'], reverse=True)
        start_hub_options = start_incentives[:5]
        stop_incentives = sorted(stop_incentives, key=lambda k: k['award'], reverse=True) 
        stop_hub_options = stop_incentives[:5]
        return start_hub_options, stop_hub_options

    def get_closest_hub(self, lat, lon):
        min_dist = 100
        
        for hub in self.hubs:
            distance = hub.get_distance(lat, lon)
            if (distance < min_dist):
                min_dist = distance  
                min_hub = hub
        
        return min_hub

    def get_closest_hubs(self, lat, lon):
        hubs = []
        current_hubs = set()
        for hub in self.hubs:
            if hub.name not in current_hubs:
                current_hubs.add(hub)
                distance = hub.get_distance(lat, lon)
                new_hub = {}
                current_hubs.add(hub.name)
                new_hub['hub'] = hub
                new_hub['dist'] = distance
                hubs.append(new_hub)

        dist_hub = sorted(hubs, key=lambda k: k['dist']) 
        return dist_hub