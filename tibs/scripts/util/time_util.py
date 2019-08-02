import datetime as dt
import math
import numpy as np

def has_overlap(start1, end1, start2, end2):
    overlap = delta_overlap(start1, end1, start2, end2)
    return overlap > dt.timedelta(0)

def delta_overlap(start1, end1, start2, end2):
    """
    Gets the time difference between the two durations

    :parameters:
        start1 (datetime): start time of the first duration
        end1 (datetime): stop time of the first duration
        start2 (datetime): start time of the second duration
        end2 (datetime): stop time of the second duration

    :returns:
        pandas timedelta class between the two durations
    """
    latest_start = max(start1, start2)
    earliest_end = min(end1, end2)
    delta = earliest_end - latest_start
    return delta

def delta_overlap_epoch(start1, end1, start2, end2):
    """
    Gets the time difference between the two durations

    :parameters:
        start1 (int): start time of the first duration in epoch
        end1 (int): stop time of the first duration in epoch
        start2 (int): start time of the second duration in epoch
        end2 (int): stop time of the second duration in epoch
        
    :returns:
        pandas timedelta class between the two durations in epoch
    """
    latest_start = max(start1, start2)
    earliest_end = min(end1, end2)
    delta = earliest_end - latest_start
    return delta

def total_time(start_times, end_times):
    """
    Gets the total time of events for the pandas datatime
    """
    differences = np.diff([start_times, end_times], axis=0)
    total = np.sum(differences)
    return total

def display_time(seconds):
    """
    Converts seconds to a string for display

    The format follows: hh:mm:ss
    """
    seconds_disp = seconds % 60
    minutes_disp = math.floor(seconds / 60) % 60
    hours_disp = math.floor(seconds / 3600) % 60
    display = '{:02d}:{:02d}:{:02d}'.format(hours_disp, minutes_disp, seconds_disp)
    return display

if __name__ == "__main__":
    start_time_1 = dt.datetime(year=2019, month=1, day=1, hour=0, minute=0, second=0)
    stop_time_1 = dt.datetime(year=2019, month=1, day=2, hour=0, minute=0, second=0)

    start_time_2 = dt.datetime(year=2019, month=1, day=1, hour=23, minute=0, second=0)
    stop_time_2 = dt.datetime(year=2019, month=1, day=2, hour=23, minute=0, second=0)

    overlap = delta_overlap(start_time_1, stop_time_1, start_time_2, stop_time_2)
    print(overlap)
    
    has_overlap = has_overlap(start_time_1, stop_time_1, start_time_2, stop_time_2)
    print(has_overlap)
    