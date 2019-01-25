# Kesavan, Kavya
# 1001-495-334
# 2018-07-10
# Assignment-03-02

import numpy as np
import matplotlib.pylab as plt


def display_numpy_array_as_table(input_array):
    # This function displays a 1d or 2d numpy array (matrix).
    if input_array.ndim == 1:
        num_of_columns, = input_array.shape
        temp_matrix = input_array.reshape((1, num_of_columns))
    elif input_array.ndim > 2:
        print("Input matrix dimension is greater than 2. Can not display as table")
        return
    else:
        temp_matrix = input_array
    number_of_rows, num_of_columns = temp_matrix.shape
    fig = plt.figure()
    tb = plt.table(cellText=np.round(temp_matrix, 2), loc=(0, 0), cellLoc='center')
    for cell in tb.properties()['child_artists']:
        cell.set_height(1/number_of_rows)
        cell.set_width(1/num_of_columns)
    ax = fig.gca()
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()
