import operator
import geopy.distance

class TripAnalysis:

    @staticmethod
    def get_favorite(keys_and_times):
        """
        Gets the favorite key based upon the most visited time

        :parameters:
            keys_and_times (dict): dictionary with keys of building and value of visited time
        :returns:
            tuple (string, int): the favorite building and time visited
        """
        favorite_building = max(keys_and_times.items(), key=operator.itemgetter(1))[0]
        return favorite_building, keys_and_times[favorite_building]

    @staticmethod
    def get_distance(start, stop):
        start_coords = (start.lat, start.lon)
        stop_coords = (stop.lat, stop.lon)
        distance = geopy.distance.vincenty(start_coords, stop_coords).miles
        return distance

    @staticmethod
    def get_distances(trip):
        """
        Gets the total distance traveled on the trip

        :returns:
            distance (double): the total distance traveled in miles
        """
        distances = []
        for visit_index in range(len(trip) - 1):
            start = trip[visit_index]    
            stop = trip[visit_index + 1]    
            coords_1 = (start.lat, start.lon)
            coords_2 = (stop.lat, stop.lon)
            distances.append(geopy.distance.vincenty(coords_1, coords_2).miles)
        return distances

    @staticmethod
    def get_total_distance(trip):
        """
        Gets the total distance traveled on the trip

        :returns:
            distance (double): the total distance traveled in miles
        """
        total_distance = 0
        for visit_index in range(len(trip) - 1):
            start = trip[visit_index]    
            stop = trip[visit_index + 1]    
            coords_1 = (start.lat, start.lon)
            coords_2 = (stop.lat, stop.lon)
            total_distance += geopy.distance.vincenty(coords_1, coords_2).miles
        return total_distance

    @staticmethod
    def get_total_duration(trip):
        """
        Gets the total duration of the trip in seconds

        The total duration will be the different between the first and last
        start times + the duration of the last trip.

        :returns:
            duration (double): the total duration of the trip in seconds
        """
        return trip[len(trip) - 1].start - trip[0].start + trip[len(trip) - 1].duration

    @staticmethod
    def filter_trips(trip):
        """
        Filters all unknown locations from the trip

        :returns:
            trip (named tuple): The trip without unknown locations
        """
        return list(filter(lambda x: x.building != None, trip))

    @staticmethod
    def add_in_trips(trip, trip_ins):
        for visit_index in range(len(trip) - 1):
            visit = trip[visit_index]
            count = trip_ins[visit.building]
            trip_ins[visit.building] = count + 1
        return trip_ins

    @staticmethod
    def add_out_trips(trip, trips_out):
        for visit_index in range(1, len(trip)):
            visit = trip[visit_index]
            count = trips_out[visit.building]
            trips_out[visit.building] = count + 1
        return trips_out
    
    @staticmethod
    def print_trip(trip):
        for index, location in zip(range(len(trip)), trip):
            print("{0}: {1}/n".format(index, location))
