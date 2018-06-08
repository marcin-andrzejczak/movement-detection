import signal_functions as sf
import plot_functions as pf
import numpy as np
import csv

# Constants
NUMBER_OF_OUTER_ENVELOPE_ITERATIONS = 2     # Best: 2
NUMBER_OF_SMOOTHENING_ITERATIONS = 1        # Best: 1
MOVEMENT_THRESHOLD_DIVIDER = 5
SAVE_PLOTS_DIRECTORY = "Results/"
FILENAMES = ["mydata.csv",
             "more_complicated_data.csv",
             "complicated_without_step.csv"]
CURRENT_FILENAME = ""


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
    plots.save_fig(SAVE_PLOTS_DIRECTORY+CURRENT_FILENAME+"_"
                   "ENV"+str(NUMBER_OF_OUTER_ENVELOPE_ITERATIONS)+"_"
                   "SMO"+str(NUMBER_OF_SMOOTHENING_ITERATIONS)+"_"
                   "THR"+str(MOVEMENT_THRESHOLD_DIVIDER)+".png")
    plots.close()


def main():
    global NUMBER_OF_OUTER_ENVELOPE_ITERATIONS
    global NUMBER_OF_SMOOTHENING_ITERATIONS
    global MOVEMENT_THRESHOLD_DIVIDER
    global CURRENT_FILENAME

    for envIter in [0, 1, 2, 3, 4]:
        NUMBER_OF_OUTER_ENVELOPE_ITERATIONS = envIter
        for smoothIter in [0, 1, 2, 3, 4]:
            NUMBER_OF_SMOOTHENING_ITERATIONS = smoothIter
            for movThreshDiv in [2, 3, 4, 5, 6]:
                MOVEMENT_THRESHOLD_DIVIDER = movThreshDiv
                for name in FILENAMES:
                    CURRENT_FILENAME = name
                    time, fx, fy, fz = read_data("data/"+name)
                    analyze_data(time, fx, fy, fz)


main()
print("END")
