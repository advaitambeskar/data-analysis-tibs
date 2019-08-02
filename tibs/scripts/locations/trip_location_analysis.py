import numpy as np
import pandas as pd

class TripLocationsAnalysis:
    def __init__(self, location_file):
        self.location_file = location_file
        self.data = pd.read_csv(location_file)
        self.hour_count = int((len(self.data.columns) - 5) / 2)
    
    def get_ranges(self, min_lat, max_lat, min_lon, max_lon):
        pos = self.data.loc[self.data['lat'] >= min_lat]
        pos = pos.loc[pos['lat'] <= max_lat]
        pos = pos.loc[pos['lon'] >= min_lon]
        pos = pos.loc[pos['lon'] <= max_lon]
        return pos['lat'], pos['lon']

    def get_latitudes_range(self, min_lat, max_lat):
        lats = self.data.loc[self.data['lat'] >= min_lat]
        lats = lats.loc[lats['lat'] <= max_lat]
        return lats['lat']
    
    def get_latitudes(self):
        return self.data['lat']

    def get_longitudes_range(self, min_lon, max_lon):
        lons = self.data.loc[self.data['lon'] >= min_lon]
        lons = lons.loc[lons['lon'] <= max_lon]
        return lons['lon']

    def get_longitudes(self):
        return self.data['lon']

    def get_trips_range(self, min_lat, max_lat, min_lon, max_lon, start=1, stop=24):
        """
        Get the total number of input and output trips for each location
        bnetween the given hours (inclusive)
        """
        data = self.data.loc[self.data['lat'] >= min_lat]
        data = data.loc[data['lat'] <= max_lat]
        data = data.loc[data['lon'] >= min_lon]
        data = data.loc[data['lon'] <= max_lon]
        total_locations = len(data.index)
        total_ins = np.zeros(total_locations)
        total_outs = np.zeros(total_locations)

        for hour in range(start, stop):
            in_name = 'in_h{0}'.format(hour)
            in_trips = data[in_name]
            total_ins += in_trips.values
            
            out_name = 'out_h{0}'.format(hour)
            out_trips = data[out_name]
            total_outs += out_trips.values

        return total_ins, total_outs

    def get_trips(self, start=1, stop=24):
        """
        Get the total number of input and output trips for each location
        bnetween the given hours (inclusive)
        """
        total_locations = len(self.data.index)
        total_ins = np.zeros(total_locations)
        total_outs = np.zeros(total_locations)

        for hour in range(start, stop):
            in_name = 'in_h{0}'.format(hour)
            in_trips = self.data[in_name]
            total_ins += in_trips.values
            
            out_name = 'out_h{0}'.format(hour)
            out_trips = self.data[out_name]
            total_outs += out_trips.values

        return total_ins, total_outs

    def get_total_trips(self):
        """
        Caculates the total number of in and out trips
        """
        all_in_trips = []
        all_out_trips = []
        for hour in range(1, self.hour_count + 1):
            in_name = 'in_h{0}'.format(hour)
            in_trips = self.data[in_name]
            hourly_ins = in_trips.sum()
            all_in_trips.append(hourly_ins)
            
            out_name = 'out_h{0}'.format(hour)
            out_trips = self.data[out_name]
            hourly_outs = out_trips.sum()
            all_out_trips.append(hourly_outs)
        return all_in_trips, all_out_trips

