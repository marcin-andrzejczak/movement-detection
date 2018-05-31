from math import pow, sqrt
import numpy as np

def get_outer_envelope(x_axis, y_axis):
    env_x = [x_axis[0], ]
    env_y = [y_axis[0], ]

    for k in range(1, len(y_axis) - 1):
        if (np.sign(y_axis[k] - y_axis[k - 1]) == 1) and (np.sign(y_axis[k] - y_axis[k + 1]) == 1):
            env_x.append(x_axis[k])
            env_y.append(y_axis[k])

    env_x.append(x_axis[-1])
    env_y.append(y_axis[-1])
    return env_x, env_y


def clean_up_peaks_in_place(x_axis, y_axis):
    for k in range(1, len(x_axis)-1):
        if x_axis[k-1] == x_axis[k] == x_axis[k+1] \
                and y_axis[k - 1] == y_axis[k + 1] \
                and y_axis[k] != y_axis[k+1]:
            y_axis[k] = y_axis[k+1]
            k += 1

    return x_axis, y_axis


def detect_by_given_threshold(x_axis, y_axis, threshold):
    detected_x = []
    detected_y = []
    for k in range(len(y_axis)):
        if y_axis[k] >= threshold:
            if k - 1 >= 0 and y_axis[k - 1] < threshold:
                detected_y.append(1)
                detected_x.append(detected_x[-1])

            detected_y.append(1)
            detected_x.append(x_axis[k])

            if k + 1 < len(y_axis) and y_axis[k + 1] < threshold:
                detected_y.append(1)
                detected_x.append(x_axis[k+1])
        else:
            detected_y.append(0)
            detected_x.append(x_axis[k])
    return detected_x, detected_y


def smoothen_signal(y_axis):
    for k in range(1, len(y_axis)-1):
        if not y_axis[k-1] <= y_axis[k] <= y_axis[k+1] and \
                not y_axis[k-1] >= y_axis[k] >= y_axis[k+1]:
            y_axis[k] = (y_axis[k-1]+y_axis[k+1])/2
    return y_axis


def calculate_resultant_portion(x, y, z):
    return sqrt(pow(sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2)) - 1, 2))
