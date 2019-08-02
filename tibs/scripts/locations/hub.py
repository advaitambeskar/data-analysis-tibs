import geopy.distance

class Hub:
    def __init__(self, id, building_name, lat, lon, cap):
        self.id = id
        self.name = building_name
        self.lat = lat
        self.lon = lon
        self.cap = cap
        self.availability = cap
        self.scale = 10

    def set_availability(self, availability):
        availability = min(availability, self.cap)
        availability = max(availability, 0)
        self.availability = availability

    def set_scale(self, scale):
        self.scale = scale

    def get_distance(self, lat, lon):
        start_coords = (lat, lon)
        stop_coords = (self.lat, self.lon)
        return geopy.distance.vincenty(start_coords, stop_coords).miles

    def surplus_incentive(self, lat, lon):
        start_coords = (lat, lon)
        stop_coords = (self.lat, self.lon)
        distance = geopy.distance.vincenty(start_coords, stop_coords).miles
        cost = self.cap - self.availability
        cost = max(cost, 0)
        award = self.scale * (1 - distance) * cost
        return award

    def shortage_incentive(self, lat, lon):
        start_coords = (lat, lon)
        stop_coords = (self.lat, self.lon)
        distance = geopy.distance.vincenty(start_coords, stop_coords).miles
        cost = self.availability - self.cap
        cost = max(cost, 0)
        award = self.scale * (1 - distance) * (1 - cost)
        return award

