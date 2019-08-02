import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import ntpath
import pandas as pd

class BluetoothAnalysis:
    def __init__(self, data_file, record_file, classic=False):
        self.data_file = data_file
        self.record_file = record_file

        self.data = pd.read_csv(self.data_file, sep='\t', header=None)
        self.records = pd.read_csv(self.record_file, sep='\t', header=None)

        if (classic):
            self.data.columns = ['timestamp', 'scanner', 'scanned', 'name', 'rssi']
        else:
            self.data.columns = ['timestamp', 'name', 'mac', 'power', 'rssi']
        
        self.records.columns = ['session', 'start', 'stop']
    

    def get_session_traces(self, session):
        return self.get_session_traces_data(session, self.data)

    def get_session_traces_data(self, session, data):
        """
        Gets the traces within the specified session number.

        The data will be obtained for multiple session numbers.
        """
        record_traces = self.records[self.records['session'] == session]
        start_times = record_traces['start'].values
        stop_times = record_traces['stop'].values

        for index, start, stop in zip(range(start_times.size), start_times, stop_times):            
            if (index == 0):
                session_data = data[(data['timestamp'] >= start) & (data['timestamp'] <= stop)]
            else:
                session_data = session_data.append(data[(data['timestamp'] >= start) & (data['timestamp'] <= stop)])

        return session_data

    def get_name_traces(self, name):
        return self.get_name_traces_data(name, self.data)
        
    def get_name_traces_data(self, name, data):
        return data[data['name'] == name]

    def get_rssi_average(self):
        return self.get_rssi_average_data(self.data)

    def get_rssi_average_data(self, data):
        return data['rssi'].mean()

    def get_datetimes(self):
        return self.get_datetimes_data(self.data)
        
    def get_datetimes_data(self, data):
        """
        Converts the timestamp volumn to an array of pandas datetimes
        """
        datetimes_utc = pd.to_datetime(data['timestamp'], unit='s')
        datetimes_est = []
        for datetime_utc in datetimes_utc:
            datetimes_est.append(datetime_utc.tz_localize('UTC').tz_convert('US/Eastern'))
        return datetimes_est
       
    def get_strings_from_dates(self, dates):
        strings = []
        for index in range(len(dates)):
            ts = dates[index]
            date_str = dt.datetime(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second).strftime('%H:%M:%S')
            strings.append(date_str)
        return strings

    def get_averaged_rssi(self):
        return self.get_averaged_rssi_data(self.data)
    
    def get_averaged_rssi_data(self, data):
        """
        Averages the rssi data for all similar timestamps
        """
        times = data['timestamp'].unique()
        average_rssi = []
        for time in times:
            rows_at_time = data[data['timestamp'] == time]
            rssi_values = rows_at_time['rssi']
            average_rssi.append(rssi_values.mean())
        return np.array(average_rssi), np.array(times)