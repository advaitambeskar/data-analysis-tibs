from analysis import BluetoothAnalysis
from sklearn.metrics import mean_absolute_error
from pynverse import inversefunc

import numpy as np
import matplotlib.pyplot as plt
import ntpath
import math

def plot_rssi_p6():
    data_files = ["../data/bluetooth_part6/BluetoothDataUltraLowPart3_2.txt",
                    "../data/bluetooth_part6/BluetoothDataLowPart3_2.txt",
                    "../data/bluetooth_part6/BluetoothDataMediumPart3_2.txt",
                    "../data/bluetooth_part6/BluetoothDataHighPart3_2.txt"]
    record_files = ["../data/bluetooth_part6/recordUltraLowPart3_2.txt",
                    "../data/bluetooth_part6/recordLowPart3_2.txt",
                    "../data/bluetooth_part6/recordMediumPart3_2.txt",
                    "../data/bluetooth_part6/recordHighPart3_2.txt"]
    device_name = 'Galaxy S8'
    plot_rssi(data_files, record_files, device_name)

def plot_rssi_p3():
    data_files = ["../data/bluetooth_part3/BluetoothDataUltraLowPart3.txt",
                    "../data/bluetooth_part3/BluetoothDataLowPart3.txt",
                    "../data/bluetooth_part3/BluetoothDataMediumPart3.txt",
                    "../data/bluetooth_part3/BluetoothDataHighPart3.txt"]
    record_files = ["../data/bluetooth_part3/recordUltraLowPart3.txt",
                    "../data/bluetooth_part3/recordLowPart3.txt",
                    "../data/bluetooth_part3/recordMediumPart3.txt",
                    "../data/bluetooth_part3/recordHighPart3.txt"]
    device_name = 'Pocophone F1'
    plot_rssi(data_files, record_files, device_name)

def plot_device_distances():
    data_files_s8 = ["../data/bluetooth_part6/BluetoothDataUltraLowPart3_2.txt",
                    "../data/bluetooth_part6/BluetoothDataLowPart3_2.txt",
                    "../data/bluetooth_part6/BluetoothDataMediumPart3_2.txt",
                    "../data/bluetooth_part6/BluetoothDataHighPart3_2.txt"]
    record_files_s8 = ["../data/bluetooth_part6/recordUltraLowPart3_2.txt",
                    "../data/bluetooth_part6/recordLowPart3_2.txt",
                    "../data/bluetooth_part6/recordMediumPart3_2.txt",
                    "../data/bluetooth_part6/recordHighPart3_2.txt"]
    data_files_poco = ["../data/bluetooth_part3/BluetoothDataUltraLowPart3.txt",
                    "../data/bluetooth_part3/BluetoothDataLowPart3.txt",
                    "../data/bluetooth_part3/BluetoothDataMediumPart3.txt",
                    "../data/bluetooth_part3/BluetoothDataHighPart3.txt"]
    record_files_poco = ["../data/bluetooth_part3/recordUltraLowPart3.txt",
                    "../data/bluetooth_part3/recordLowPart3.txt",
                    "../data/bluetooth_part3/recordMediumPart3.txt",
                    "../data/bluetooth_part3/recordHighPart3.txt"]
            
    device_name_s8 = 'Galaxy S8'        
    device_name_poco = 'Pocophone F1'
    distances = [0.5, 1, 5, 10, 20, 25, 30]
    classic = False
    
    fig_model, ax_model = plt.subplots(2, 2, sharex=True, sharey=True)
    plt.gcf().subplots_adjust(bottom=0.15, left=0.1)

    for index, data_file_s8, record_file_s8, data_file_poco, record_file_poco in zip(range(len(data_files_s8)), data_files_s8, record_files_s8, data_files_poco, record_files_poco):
        analysis_s8 = BluetoothAnalysis(data_file_s8, record_file_s8, classic)
        analysis_poco = BluetoothAnalysis(data_file_poco, record_file_poco, classic)

        # Calculate average mean for s8
        means = []
        for session in analysis_s8.records['session']:
            records = analysis_s8.get_session_traces(session)
            records = analysis_s8.get_name_traces_data(device_name_s8, records)
            means.append(analysis_s8.get_rssi_average_data(records))
            
        row = (int)(index / 2)
        col = (int)(index % 2)
        ax_model[row, col].plot(distances, means)

        if (index == 0):
            smaller_value = np.amax(means)
            higher_value = np.amin(means)
        else:
            smaller_value = max(np.amax(means), smaller_value)
            higher_value = min(np.amin(means), higher_value)

        # Calculate average mean for poco
        means = []
        for session in analysis_poco.records['session']:
            records = analysis_poco.get_session_traces(session)
            records = analysis_poco.get_name_traces_data(device_name_poco, records)
            means.append(analysis_poco.get_rssi_average_data(records))

        row = (int)(index / 2)
        col = (int)(index % 2)
        ax_model[row, col].plot(distances, means)

        if (index == 0):
            smaller_value = np.amax(means)
            higher_value = np.amin(means)
        else:
            smaller_value = max(np.amax(means), smaller_value)
            higher_value = min(np.amin(means), higher_value)

    
    fig_model.suptitle('RSSI Level versus Distance')
    ax_model[0, 0].set_title("Ultra Low")
    ax_model[0, 0].set_ylabel('RSSI')
    ax_model[0, 0].legend([device_name_s8, device_name_poco])
    ax_model[0, 1].set_title("Low")
    ax_model[0, 1].legend([device_name_s8, device_name_poco])
    ax_model[1, 0].set_title("Medium")
    ax_model[1, 0].set_ylabel('RSSI')
    ax_model[1, 0].set_xlabel('Distance (meters)')
    ax_model[1, 0].legend([device_name_s8, device_name_poco])
    ax_model[1, 1].set_title("High")
    ax_model[1, 1].set_xlabel('Distance (meters)')
    ax_model[1, 1].legend([device_name_s8, device_name_poco])

    plt.show(block=True)

def fit_line():
    data_file_s8 = "../data/bluetooth_part6/BluetoothDataHighPart3_2.txt"
    record_file_s8 = "../data/bluetooth_part6/recordHighPart3_2.txt"
    data_file_poco = "../data/bluetooth_part3/BluetoothDataHighPart3.txt"
    record_file_poco = "../data/bluetooth_part3/recordHighPart3.txt"
            
    device_name_s8 = 'Galaxy S8'        
    device_name_poco = 'Pocophone F1'
    distances = [0.5, 1, 5, 10, 20, 25, 30]
    classic = False

    analysis_s8 = BluetoothAnalysis(data_file_s8, record_file_s8, classic)
    analysis_poco = BluetoothAnalysis(data_file_poco, record_file_poco, classic)

    means_s8 = []
    for session in analysis_s8.records['session']:
        records = analysis_s8.get_session_traces(session)
        records = analysis_s8.get_name_traces_data(device_name_s8, records)
        means_s8.append(analysis_s8.get_rssi_average_data(records))
        
    means_poco = []
    for session in analysis_poco.records['session']:
        records = analysis_poco.get_session_traces(session)
        records = analysis_poco.get_name_traces_data(device_name_poco, records)
        means_poco.append(analysis_poco.get_rssi_average_data(records))

    s8_model = fit_model(distances, means_s8, device_name_s8)
    poco_model = fit_model(distances, means_poco, device_name_poco)
    average_model = fit_average_model(distances, means_s8, means_poco)

    return s8_model, poco_model, average_model

def fit_model(distances, mean, device):
    z = np.polyfit(distances, mean, 3)
    model = np.poly1d(z)
    model_x = np.linspace(distances[0], distances[-1], 50)
    model_y = model(model_x)

    fig, ax = plt.subplots(1, 1)
    plt.gcf().subplots_adjust(bottom=0.15, left=0.1)
    ax.plot(distances, mean)
    ax.plot(model_x, model_y)
    legend = [device, 'Model']
    fig.suptitle('3rd Degree Polynomial Fit for the {0} RSSI at Various Distances'.format(device))
    ax.set_xlabel('Distance (meters)')
    ax.set_ylabel('RSSI')
    ax.legend(legend)
    print('Model for the {0}: \n{1}'.format(device, model))
    return model
 
def fit_average_model(distances, mean_1, mean_2):
    all_means = np.mean( np.array([ mean_1, mean_2 ]), axis=0 )
    z = np.polyfit(distances, all_means, 3)
    model = np.poly1d(z)
    model_x = np.linspace(distances[0], distances[-1], 50)
    model_y = model(model_x)

    fig, ax = plt.subplots(1, 1)
    plt.gcf().subplots_adjust(bottom=0.15, left=0.1)
    ax.plot(distances, mean_1)
    ax.plot(distances, mean_2)
    ax.plot(model_x, model_y)
    legend = ['Galaxy S8', 'Pocophone F1', 'Model']
    fig.suptitle('3rd Degree Polynomial Fit for the Average RSSI')
    ax.set_xlabel('Distance (meters)')
    ax.set_ylabel('RSSI')
    ax.legend(legend)
    print('General Model: \n{0}'.format(model))
    return model

def plot_rssi(data_files, record_files, device_name):
    distances = [0.5, 1, 5, 10, 20, 25, 30]
    model_distances = [0.5, 1, 2, 5, 7.5, 10, 12.5, 15, 20, 25, 30]
    classic = False
    
    fig_rssi, ax_rssi = plt.subplots(1, 1)
    plt.gcf().subplots_adjust(bottom=0.15, left=0.1)
    fig_model, ax_model = plt.subplots(2, 2, sharex=True, sharey=True)
    plt.gcf().subplots_adjust(bottom=0.15, left=0.1)
    fig_error, ax_error = plt.subplots(1, 1)
    plt.gcf().subplots_adjust(bottom=0.15, left=0.1)

    mean_errors = []
    for index, data_file, record_file in zip(range(len(data_files)), data_files, record_files):
        analysis = BluetoothAnalysis(data_file, record_file, classic)

        # Calculate average mean
        means = []
        for session in analysis.records['session']:
            records = analysis.get_session_traces(session)
            records = analysis.get_name_traces_data(device_name, records)
            means.append(analysis.get_rssi_average_data(records))
        ax_rssi.plot(distances, means)

        if (index == 0):
            smaller_value = np.amax(means)
            higher_value = np.amin(means)
        else:
            smaller_value = max(np.amax(means), smaller_value)
            higher_value = min(np.amin(means), higher_value)

        # Generate log shadowing models for line plotting
        log_shadowing_values_plot = compute_log_shadowing(model_distances, means[1])
        row = (int)(index / 2)
        col = (int)(index % 2)
        ax_model[row, col].plot(distances, means)
        ax_model[row, col].plot(model_distances, log_shadowing_values_plot)

        # Generate log shadowing models for error plotting
        log_shadowing_values = compute_log_shadowing(distances, means[1])
        print("Means: {0}".format(means[1]))

        truths = []
        actuals = []
        for mean, truth in zip(means, log_shadowing_values):
            if (not math.isnan(mean)):
                truths.append(truth)
                actuals.append(mean)

        mean_errors.append(mean_absolute_error(truths, actuals))

    legend = ['Ultra Low', 'Low', 'Medium', 'High']
    fig_rssi.suptitle('Average RSSI Level versus Distance at Different Advertising Settings ({0})'.format(device_name))
    ax_rssi.set_xlabel('Distance (meters)')
    ax_rssi.set_ylabel('RSSI')
    ax_rssi.legend(legend)
    ax_rssi.set_ylim([higher_value * 1.05, smaller_value * 0.95])
    
    fig_model.suptitle('RSSI Level versus Distance with Log Shadowing Model ({0})'.format(device_name))
    ax_model[0, 0].set_title("Ultra Low")
    ax_model[0, 0].set_ylabel('RSSI')
    ax_model[0, 0].legend(['Measured', 'Log Shadowing'])
    ax_model[0, 1].set_title("Low")
    ax_model[0, 1].legend(['Measured', 'Log Shadowing'])
    ax_model[1, 0].set_title("Medium")
    ax_model[1, 0].set_ylabel('RSSI')
    ax_model[1, 0].set_xlabel('Distance (meters)')
    ax_model[1, 0].legend(['Measured', 'Log Shadowing'])
    ax_model[1, 1].set_title("High")
    ax_model[1, 1].set_xlabel('Distance (meters)')
    ax_model[1, 1].legend(['Measured', 'Log Shadowing'])

    fig_error.suptitle('Mean Absolute Error of the Recorded Data versus the Log Shadowing Model ({0})'.format(device_name))
    ax_error.bar(legend, mean_errors)
    ax_error.set_xlabel("Power Setting")
    ax_error.set_ylabel("Mean Absolute Error")
    highest_error = np.amax(mean_errors)
    ax_error.set_ylim([0, math.ceil(highest_error * 1.05)])

    plt.show(block=True)

def compute_log_shadowing(distances, mean):
    values = []
    n = 2   # Path loss exponent in free space
    for distance in distances:
        values.append(-10 * n * math.log10(distance) + mean)
    return values

def compute_log_shadowing_distances(rssis, mean):
    n = 2
    value = 10**((rssis - mean) / -10 * n)
    return value

def scenario_prediction_1(model_1, model_2):
    # Scenario part 4 1
    data_file_classic = "../data/bluetooth_part4/BluetoothDataClassicPart4_1.txt"
    record_file_classic = "../data/bluetooth_part4/recordClassicPart4_1.txt"
    data_files_ble = "../data/bluetooth_part4/BluetoothDataBlePart4_1.txt"
    record_files_ble = "../data/bluetooth_part4/recordBlePart4_1.txt"
    scenario = 1
    scenario_prediction(data_file_classic, record_file_classic, data_files_ble, record_files_ble, 1, model_1, model_2)


def scenario_prediction_2(model_1, model_2):
    # Scenario part 4 2
    data_file_classic = "../data/bluetooth_part4/BluetoothDataClassicPart4_2.txt"
    record_file_classic = "../data/bluetooth_part4/recordClassicPart4_2.txt"
    data_files_ble = "../data/bluetooth_part4/BluetoothDataBlePart4_2.txt"
    record_files_ble = "../data/bluetooth_part4/recordBlePart4_2.txt"
    scenario = 2
    scenario_prediction(data_file_classic, record_file_classic, data_files_ble, record_files_ble, 2, model_1, model_2)


def scenario_prediction(classic_data, classic_record, ble_data, ble_record, title, model_1, model_2):
    # Classic Analysis
    device_name = 'Pocophone F1'

    analysis = BluetoothAnalysis(classic_data, classic_record, True)

    max_time_difference = 0
    largest_value = -100
    smallest_value = 0
    for session in analysis.records['session']:
        records = analysis.get_session_traces(session)
        records = analysis.get_name_traces_data(device_name, records)
        
        rssi, times = analysis.get_averaged_rssi_data(records)
        largest_value = max(np.max(records['rssi']), largest_value)
        smallest_value = min(np.min(records['rssi']), smallest_value)
        min_time = np.min(records['timestamp'])
        max_time = np.max(records['timestamp'])
        classic_rssi = rssi
        classic_times = times - min_time
        time_difference = max_time - min_time
        max_time_difference = max(time_difference, max_time_difference)
    
    # BLE Analysis
    analysis = BluetoothAnalysis(ble_data, ble_record, False)

    ble_rssis = []
    ble_times = []
    for session in analysis.records['session']:
        records = analysis.get_session_traces(session)
        records = analysis.get_name_traces_data(device_name, records)

        rssi, times = analysis.get_averaged_rssi_data(records)
        largest_value = max(np.max(records['rssi']), largest_value)
        smallest_value = min(np.min(records['rssi']), smallest_value)
        min_time = np.min(records['timestamp'])
        max_time = np.max(records['timestamp'])
        ble_rssis.append(rssi)
        ble_times.append(times - min_time)
        time_difference = max_time - min_time
        max_time_difference = max(time_difference, max_time_difference)

    fig_rssi, ax_rssi = plt.subplots(1, 1)
    plt.gcf().subplots_adjust(bottom=0.15, left=0.1)
    ax_rssi.set_xlabel('Time (seconds)')
    ax_rssi.set_ylabel('RSSI')
    if (title == 1):
        fig_rssi.suptitle('RSSI Analysis without Stopping')
    else:        
        fig_rssi.suptitle('RSSI Analysis when Stopping for 1 Minute')

    # Classic plot
    plt.plot(classic_times, classic_rssi, marker='o')

    # BLE plots
    for ble_rssi, ble_time in zip(ble_rssis, ble_times):
        plt.plot(ble_time, ble_rssi, marker='o')

    ax_rssi.set_ylim([math.ceil(smallest_value * 1.05), largest_value * 0.95])
    ax_rssi.legend(['Classic', 'Ultra Low', 'Low', 'Medium', 'High'])

    # Now calculate distances using model 1
    fig_dist_1, ax_dist_1 = plt.subplots(1, 1)
    plt.gcf().subplots_adjust(bottom=0.15, left=0.1)
    ax_dist_1.set_xlabel('Time (seconds)')
    ax_dist_1.set_ylabel('Distance (meters)')
    if (title == 1):
        fig_dist_1.suptitle("Estimated Distance using the General Model (Scenario #1)")
    else:        
        fig_dist_1.suptitle("Estimated Distance using the General Model (Scenario #2)")

    min_distance = 100
    for ble_rssi, ble_time in zip(ble_rssis, ble_times):
        distances = model_1(ble_rssi)
        min_distance = min(distances)
        plt.plot(ble_time, distances, marker='o')

    ax_dist_1.set_ylim(min_distance * 1.05, 17)
    ax_dist_1.legend(['Ultra Low', 'Low', 'Medium', 'High'])
    
    # Now calculate distances using model 2
    fig_dist_2, ax_dist_2 = plt.subplots(1, 1)
    plt.gcf().subplots_adjust(bottom=0.15, left=0.1)
    ax_dist_2.set_xlabel('Time (seconds)')
    ax_dist_2.set_ylabel('Distance (meters)')
    if (title == 1):
        fig_dist_2.suptitle("Estimated Distance using the Pocophone Model (Scenario #1)")
    else:        
        fig_dist_2.suptitle("Estimated Distance using the Pocophone Model (Scenario #2)")

    min_distance = 100
    for ble_rssi, ble_time in zip(ble_rssis, ble_times):
        distances = model_2(ble_rssi)
        min_distance = min(distances)
        plt.plot(ble_time, distances, marker='o')

    ax_dist_2.set_ylim(min_distance * 1.05, 17)
    ax_dist_2.legend(['Ultra Low', 'Low', 'Medium', 'High'])
    
    # Now calculate distances using log shadow model
    fig_dist_3, ax_dist_3 = plt.subplots(1, 1)
    plt.gcf().subplots_adjust(bottom=0.15, left=0.1)
    ax_dist_3.set_xlabel('Time (seconds)')
    ax_dist_3.set_ylabel('Distance (meters)')
    if (title == 1):
        fig_dist_3.suptitle("Estimated Distance using the Log Shadowing Model (Scenario #1)")
    else:        
        fig_dist_3.suptitle("Estimated Distance using the Log Shadowing Model (Scenario #2)")

    min_distance = 100

    # Hardcoded means calculated in previous parts
    means = [-94.11111111111111, -83.75, -87.96078431372548, -84.31111111111112]
    for ble_rssi, ble_time, mean in zip(ble_rssis, ble_times, means):
        distances = compute_log_shadowing_distances(ble_rssi, mean)
        min_distance = min(distances)
        plt.plot(ble_time, distances, marker='o')

    distances = compute_log_shadowing_distances(classic_rssi, -58.6)
    plt.plot(classic_times, distances, marker='o')

    ax_dist_3.set_ylim(min_distance * 1.05, 20)
    ax_dist_3.legend(['Ultra Low', 'Low', 'Medium', 'High'])

if __name__ == "__main__":
    style_file = '../style/simple_charts.mplstyle'
    if (ntpath.isfile(style_file)):
        plt.style.use(style_file)

    galaxy_s8, poco_phone, general_model = fit_line()
    inverse_general = inversefunc(general_model)
    inverse_poco = inversefunc(poco_phone)
    scenario_prediction_1(inverse_general, inverse_poco)
    scenario_prediction_2(inverse_general, inverse_poco)
    
    plt.show(block=True)