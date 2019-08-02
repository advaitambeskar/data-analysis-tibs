from dhcp import dhcp_activity as dhcp
from dhcp import dhcp_filters as dhcpf
from locations import trip_analysis as tripa
from locations import trip_location_analysis as loca
from locations import location_plot as locp
from locations import location_writer as locw
from locations import route
from locations import hubs
from util import image_util as imageu
from util import time_util as timeu

from colour import Color

import datetime as dt
import matplotlib.pyplot as plt
import ntpath
import pandas as pd
import gmplot
import numpy as np
import math

# TODO look into density modular
# TODO construct densitiy information for paths at specific times
# TODO get distance between paths (for now use WGS84 reference elipsoid, but later explain how this can be modified for google map routes)
# TODO construct weighted routes between notes based upon density, and map routes
# TODO difficulty in determining whether a trip is the start of a new day, or if the user just
# stayed at the last location for a long time. For this, we can just assume that this is a trip,
# since the user will take a trip if it is the next day.
def total_trips_analysis():
    saturday_trip = 'data/dhcp/locations/20120407_saturday_locations.csv'
    saturday_analysis = loca.TripLocationsAnalysis(saturday_trip)
    saturday_ins, saturday_outs = saturday_analysis.get_total_trips()
    sunday_trip = 'data/dhcp/locations/20120408_sunday_locations.csv'
    sunday_analysis = loca.TripLocationsAnalysis(sunday_trip)
    sunday_ins, sunday_outs = sunday_analysis.get_total_trips()
    monday_trip = 'data/dhcp/locations/20120409_monday_locations.csv'
    monday_analysis = loca.TripLocationsAnalysis(monday_trip)
    monday_ins, monday_outs = monday_analysis.get_total_trips()
    tuesday_trip = 'data/dhcp/locations/20120410_tuesday_locations.csv'
    tuesday_analysis = loca.TripLocationsAnalysis(tuesday_trip)
    tuesday_ins, tuesday_outs = tuesday_analysis.get_total_trips()
    wednesday_trip = 'data/dhcp/locations/20120411_wednesday_locations.csv'
    wednesday_analysis = loca.TripLocationsAnalysis(wednesday_trip)
    wednesday_ins, wednesday_outs = wednesday_analysis.get_total_trips()
    thursday_trip = 'data/dhcp/locations/20120412_thursday_locations.csv'
    thursday_analysis = loca.TripLocationsAnalysis(thursday_trip)
    thursday_ins, thursday_outs = thursday_analysis.get_total_trips()
    friday_trip = 'data/dhcp/locations/20120413_friday_locations.csv'
    friday_analysis = loca.TripLocationsAnalysis(friday_trip)
    friday_ins, friday_outs = friday_analysis.get_total_trips()

    weekly_ins = saturday_ins + sunday_ins + monday_ins + tuesday_ins + wednesday_ins + thursday_ins + friday_ins
    weekly_outs = saturday_outs + sunday_outs + monday_outs + tuesday_outs + wednesday_outs + thursday_outs + friday_outs

    start_epoch = 1333756800
    stop_epoch = 1334361600
    number_of_hours = math.ceil((stop_epoch - start_epoch) / 3600) + 1
    earliest_time = pd.to_datetime(start_epoch, unit='s')
    latest_time = pd.to_datetime(stop_epoch, unit='s')
    bins = pd.date_range(start=earliest_time, end=latest_time, periods=number_of_hours)
      
    strings = []
    for index in range(bins.size):
        ts = bins[index]
        date_str = dt.datetime(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second).strftime('%a %H')
        strings.append(date_str)
    
    locp.LocationPlot.plot_in_out_trips(weekly_outs, weekly_ins, strings)

def trips_per_location():
    saturday_trip = 'data/dhcp/locations/20120407_saturday_locations.csv'
    saturday_analysis = loca.TripLocationsAnalysis(saturday_trip)
    monday_trip = 'data/dhcp/locations/20120409_monday_locations.csv'
    monday_analysis = loca.TripLocationsAnalysis(monday_trip)
    tuesday_trip = 'data/dhcp/locations/20120410_tuesday_locations.csv'
    tuesday_analysis = loca.TripLocationsAnalysis(tuesday_trip)

    min_lat = 29.6376
    max_lat = 29.6569
    min_lon = -82.3567
    max_lon = -82.3355
    hours = 6
    day = 'output/saturday'
    for index in range(1, 5):
        lats_more = saturday_analysis.get_latitudes()
        lats, lons = saturday_analysis.get_ranges(min_lat, max_lat, min_lon, max_lon)
        start_time = (index - 1) * hours + 1
        stop_time = index * hours + 1
        file_name = '{0}_{1}_{2}'.format(day, start_time, stop_time)
        ins, outs = saturday_analysis.get_trips_range(min_lat, max_lat, min_lon, max_lon, start_time, stop_time)
        locp.LocationPlot.plot_building_heatmap(lats, lons, outs, file_name)
    day = 'output/monday'
    for index in range(1, 5):
        lats, lons = monday_analysis.get_ranges(min_lat, max_lat, min_lon, max_lon)
        start_time = (index - 1) * hours + 1
        stop_time = index * hours + 1
        file_name = '{0}_{1}_{2}'.format(day, start_time, stop_time)
        ins, outs = monday_analysis.get_trips_range(min_lat, max_lat, min_lon, max_lon, start_time, stop_time)
        locp.LocationPlot.plot_building_heatmap(lats, lons, outs, file_name)
    day = 'output/tuesday'
    for index in range(1, 5):
        lats, lons = tuesday_analysis.get_ranges(min_lat, max_lat, min_lon, max_lon)
        start_time = (index - 1) * hours + 1
        stop_time = index * hours + 1
        file_name = '{0}_{1}_{2}'.format(day, start_time, stop_time)
        ins, outs = tuesday_analysis.get_trips_range(min_lat, max_lat, min_lon, max_lon, start_time, stop_time)
        locp.LocationPlot.plot_building_heatmap(lats, lons, outs, file_name)

def filter_traces():
    location_file = "data/prefix_lat_lon_name_category_main_campus.csv"
    dhcp_file = "D:/Development/data/dhcp/DHCP_April_2012_ANON_MAC.csv"
    refined_file = "20120413_buildings_refined.csv"
    analysis = dhcp.DHCPAnalysis(dhcp_file, location_file)

    # Sunday
    # start = 1333843200
    # stop = 1333933199

    # Tuesday
    # start = 1334016000
    # stop =  1334105999

    # Wednesday
    # start = 1334102400
    # stop =  1334192399

    # Thursday
    # start = 1334188800
    # stop =  1334278799

    # Friday
    start = 1334275200
    stop =  1334365199

    traces = dhcpf.DHCPFilters().filter_time_range(analysis.traces, start, stop)
    print("Adding buildings")
    dhcpf.DHCPFilters().write_traces_building_names(traces, location_file, refined_file)

def show_path():
    dhcp_file = "data/dhcp/20120409_buildings.csv"
    location_file = "data/prefix_lat_lon_name_category_main_campus.csv"
    analysis = dhcp.DHCPAnalysis(dhcp_file, location_file)

    start_user = 76
    stop_user = 76
    users = range(start_user, stop_user + 1)
    colors = list(Color("#c92318").range_to(Color("#45c6f9"), len(users)))
    gmap = gmplot.GoogleMapPlotter(29.645,-82.355, 13)
    for user_id in users:
        trip = analysis.get_user_trip(user_id)
        trip = tripa.TripAnalysis.filter_trips(trip)
        if (len(trip) > 0):
            color = colors[user_id - start_user]
            locp.LocationPlot.plot_trip(gmap, trip, color, True, True)
            gmap.draw("map_trip_full_{0}.html".format(user_id))
            refined_trip = dhcp.DHCPAnalysis.trace_refine_trip(trip, 60, 0.5)
            locp.LocationPlot.plot_trip(gmap, refined_trip, color, True, True)
            gmap.draw("map_trip_refined_{0}.html".format(user_id))
            # print("User: {0}".format(user_id))
            # for index, location in zip(range(len(trip)), trip):
            #     print("{0}: {1}".format(index, location))
            #     print()
            for index, location in zip(range(len(trip)), trip):
                building = trip[index].building
                time_sense_last = 0
                distance = 0
                if (index < len(trip) - 1):
                    time_sense_last = trip[index + 1].start - trip[index].start
                if (index != 0):
                    distance = tripa.TripAnalysis.get_distance(trip[index - 1], trip[index])
                print('{0},{1},{2}'.format(building,  timeu.display_time(time_sense_last), distance))

def create_route():
    start = route.Hub(id=1, name='Marston', lat=29.647957, lon=-82.343904)
    stop = route.Hub(id=2, name='New Engineering Building', lat=29.642287, lon=-82.347076)
    route = route.Route(start, stop, 100)
    print(route)

def animated_trip_heatmap():
    dhcp_file = "./data/dhcp/locations/20120413_friday_locations.csv"
    
    traces = pd.read_csv(dhcp_file)
    lats = traces['lat']
    lons = traces['lon']
    stop_index = 25
    for hour in range(1, stop_index):
        hour_str = 'out_h{0}'.format(hour)
        trips = traces[hour_str]
        heatmap_file = './output/{0}_{1}'.format('20120413', hour_str)
        locp.LocationPlot.generate_heatmap(lats, lons, trips, heatmap_file)
        print("Finished {0} / {1}".format(hour, stop_index - 1))

    print("Merging")
    outputfile = imageu.ImageUtil.convert_images_to_gif("./output", 200)
    locp.LocationPlot.create_map_overlay(lats, lons, outputfile, 'map_week')
    print("Finished")

def calculate_routes():
    location_file = "./data/dhcp/locations/20120413_friday_locations.csv"
    all_hubs = hubs.Hubs(location_file)

    # Marston to New Engineering Building
    # start_lat = 29.647957	
    # start_lon = -82.343904
    # stop_lat = 29.642287	
    # stop_lon = -82.347076
    # hour = 15

    # Reitz to Innovation
    # start_lat = 29.646386
    # start_lon = -82.34779
    # stop_lat = 29.649981	
    # stop_lon = -82.332703
    # hour = 15
    
    # Innovation to Reitz
    start_lat = 29.649981	
    start_lon = -82.332703
    stop_lat = 29.646386
    stop_lon = -82.34779
    hour = 15

    starts, stops = all_hubs.determine_routes(start_lat, start_lon, stop_lat, stop_lon, hour)

    print('Start hubs: ')
    for start in starts:
        print('Building: {0}\tAward: {1}\tDistance: {2} miles'.format(start['hub'].name, round(start['award'], 2), round(start['distance'], 4)))
    print('')
    print('Destination hubs: ')
    for stop in stops:
        print('Building: {0}\tAward: {1}\tDistance: {2} miles'.format(stop['hub'].name, round(stop['award'], 2), round(stop['distance'], 4)))


if __name__ == "__main__":
    style_file = 'style/report_simple.mplstyle'
    if (ntpath.isfile(style_file)):
        plt.style.use(style_file)

    calculate_routes()