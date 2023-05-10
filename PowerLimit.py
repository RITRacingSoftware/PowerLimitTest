"""
RIT Racing
PowerLimit checks from the input text file ( in this case the can logger given file)

"""

from fileinput import filename
import fdplib.darab as darab


"""The maximum wattage allowed"""
LIMITWATTS = 80000


def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def ReadPowerValues(file: filename, stepSize: float):
    data = darab.DarabData(file)


"""PowerLimit function checks if the power is above the the given threshold for 100ms 
or the moving average is above the the limit, return false"""


def PowerLimit(data):

    while True:
        if 0"""placeholder""" > LIMITWATTS or moving_average(data) > LIMITWATTS:
            return True


def main():
    file = input("Enter the file name (filename.txt):")
    stepSize = input("Enter the time step size (0.1 is 100ms):")
    data = darab.DarabData(file)

    if (PowerLimit):
        print("Power Limit was exceeded")
    else:
        print("Power Limit was not exceeded")


if __name__ == "__main__":
    main()
