"""
RIT Racing
PowerLimit checks from the input text file ( in this case the can logger given file)

"""

from fileinput import filename
import fdplib.darab as darab
import numpy as np

FILENAME = "F30_5_55_23_energy_check.txt"


"""The maximum wattage allowed"""
LIMITWATTS = 76000  # 80000

"""The step size in the .txt file exported from Windarab"""
STEP_SIZE = 0.001

"""The moving average time over which the power can't be over the limit for the rules"""
MOVING_AVERAGE_TIME_S = 0.500

"""The maximum continuous time that the power can be over the limit for"""
CONITNUOUS_POWER_TIME_S = 0.100


def moving_average(array, window_size):
    # i = 0
    # # Initialize an empty list to store moving averages
    # moving_averages = []

    # # Loop through the array to
    # # consider every window of size window_size
    # while i < len(array) - window_size + 1:

    #     window = array[i: i + window_size]

    #     # Calculate the average of current window
    #     window_average = round(sum(window) / window_size, 2)

    #     # Store the average of current
    #     # window in moving average list
    #     moving_averages.append(window_average)

    #     # Shift window to right by one position
    #     i += 1

    # # print(moving_averages)
    # return moving_averages
    ret = np.cumsum(array, dtype=float)
    ret[window_size:] = ret[window_size:] - ret[:-window_size]
    return ret[window_size - 1:] / window_size


def num_moving_average_violations(data_array):
    num_steps_for_violation = MOVING_AVERAGE_TIME_S / STEP_SIZE
    num_steps_for_violation = int(num_steps_for_violation)
    print(num_steps_for_violation)
    moving_averages = moving_average(data_array, num_steps_for_violation)
    num_violations = 0
    for i in moving_averages:
        if i > LIMITWATTS:
            num_violations += 1

    return num_violations


def num_continuous_violations(data_array):
    num_violations = 0
    num_steps_for_violation = CONITNUOUS_POWER_TIME_S / STEP_SIZE
    num_steps_for_violation = int(num_steps_for_violation)
    print(num_steps_for_violation)
    num_steps_over_limit = 0
    for i in data_array:
        if num_steps_over_limit < num_steps_for_violation:
            if (i > LIMITWATTS):
                num_steps_over_limit += 1
            else:
                num_steps_over_limit = 0
        elif num_steps_over_limit == num_steps_for_violation:
            num_violations += 1
    return num_violations


# def ReadPowerValues(file: filename, stepSize: float):
#     data = darab.DarabData(file)


"""PowerLimit function checks if the power is above the the given threshold for 100ms 
or the moving average is above the the limit, return false"""


# def PowerLimit(data):

#     while True:
#         if 0"""placeholder""" > LIMITWATTS or moving_average(data) > LIMITWATTS:
#             return True


def main():
    file = FILENAME  # input("Enter the file name (filename.txt):")
    # stepSize =  STEP_SIZE # input("Enter the time step size (0.1 is 100ms):")
    data = darab.DarabData(file)

    current_data = data.get_var_np("BmsInstCurrentFilt")
    pack_voltage_data = data.get_var_np("BmsStatus_PackVoltage")
    power_data = [a*b for a, b in zip(current_data, pack_voltage_data)]

    num_moving_avg_violations = num_moving_average_violations(power_data)
    num_cont_violations = num_continuous_violations(power_data)

    print("Number of continuous vioations: %d" %
          num_cont_violations)
    print("Number of moving average vioations: %d" % num_moving_avg_violations)

    # if (PowerLimit):
    #     print("Power Limit was exceeded")
    # else:
    #     print("Power Limit was not exceeded")


if __name__ == "__main__":
    main()
