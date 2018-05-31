import signal_functions as sf
import plot_functions as pf
import numpy as np
import csv

# Constants
NUMBER_OF_OUTER_ENVELOPE_ITERATIONS = 2
NUMBER_OF_SMOOTHENING_ITERATIONS = 1
MOVEMENT_THRESHOLD_DIVIDER = 5
FILENAMES = ["mydata.csv",
             "more_complicated_data.csv",
             "complicated_without_step.csv"]


def read_data(filename, delimiter=",", newline=''):
    x_axis = []
    tx = []
    ty = []
    tz = []
    with open(filename, newline=newline) as csvfile:
        # Read all the data
        reader = csv.reader(csvfile, delimiter=delimiter)
        next(reader)
        for row in list(reader):
            if '' not in row:
                # Convert data to correct format
                data = [float(number) for number in row]
                x_axis.append(data[0])
                tx.append(data[1])
                ty.append(data[2])
                tz.append(data[3])

    return x_axis, tx, ty, tz


def analyze_data(x_axis, tx, ty, tz):
    resultant = np.array([sf.calculate_resultant_portion(tx[p], ty[p], tz[p]) for p in range(len(x_axis))])
    for _ in range(NUMBER_OF_SMOOTHENING_ITERATIONS):
        resultant = sf.smoothen_signal(resultant)

    env_x, env_y = sf.get_outer_envelope(x_axis, resultant)
    for _ in range(NUMBER_OF_OUTER_ENVELOPE_ITERATIONS):
        env_x, env_y = sf.get_outer_envelope(env_x, env_y)

    movement_threshold = max(env_y) / MOVEMENT_THRESHOLD_DIVIDER

    movement_x, movement_y = sf.detect_by_given_threshold(env_x, env_y, movement_threshold)
    movement_x, movement_y = sf.clean_up_peaks_in_place(movement_x, movement_y)

    plots = pf.Subplots(3, 1)
    plots.add_plot(0, 0, x_axis, resultant, "Resultant", "Time", "Resultant")
    plots.add_plot(1, 0, env_x, env_y, "Envelope", "Time", "Envelope")
    plots.add_plot(2, 0, movement_x, movement_y, "Movement", "Time", "Movement")
    plots.show()


def main():
    for name in FILENAMES:
        time, fx, fy, fz = read_data("data/"+name)
        analyze_data(time, fx, fy, fz)


main()
