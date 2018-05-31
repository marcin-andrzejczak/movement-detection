import matplotlib.pyplot as plt


class Subplots(object):

    def __init__(self, rows, cols):
        figure , plots = plt.subplots(rows, cols)
        self.plots = plots
        self.rows = rows
        self.cols = cols
        self.figure = figure

    def add_plot(self, row, col, x_axis, y_axis, title=None, x_label=None, y_label=None):
        position = (row, col) if self.cols > 1 else row
        self.plots[position].plot(x_axis, y_axis)
        self.plots[position].set_title(title if title is not None else "")
        self.plots[position].set_xlabel(x_label if x_label is not None else "")
        self.plots[position].set_ylabel(y_label if y_label is not None else "")

    def show(self):
        self.figure.show()
