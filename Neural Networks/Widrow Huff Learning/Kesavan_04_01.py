# Kesavan, Kavya
# 1001-495-334
# 2018-10-29
# Assignment-04-01

import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy.linalg import inv
import os
import numpy as np


class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.center_frame = tk.Frame(self)
        self.left_frame = Widrow_Huff(self, self.center_frame)
        self.center_frame.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.center_frame.grid_propagate(True)
        self.center_frame.rowconfigure(1, weight=1, uniform='xx')
        self.center_frame.columnconfigure(0, weight=1, uniform='xx')
        self.center_frame.columnconfigure(1, weight=1, uniform='xx')
        self.left_frame.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)


class Widrow_Huff(tk.Frame):
    def __init__(self, root, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.root = root

        # Variable declarations
        self.weights = np.array([])
        self.bias = np.array([])
        self.dataset = np.array([])
        self.R = np.array([])
        self.h = np.array([])
        self.stationary_pt = np.array([])
        self.training_samples = np.array([])
        self.testing_samples = np.array([])
        self.training_target = np.array([])
        self.testing_target = np.array([])
        self.delayed_elements = 2
        self.iterations = 10
        self.train_sample_size = 80
        self.learning_rate = 0.1
        self.stride = 2
        self.r = 0

        # 2 Plots
        self.xmin = 0
        self.xmax = 10
        self.ymin = 0
        self.ymax = 10
        figure_size = (8, 4)
        self.plot_frame = tk.Frame(self.master)
        self.plot_frame.grid(row=0, column=0)
        self.figure = plt.figure(figsize=figure_size)
        self.axes = self.figure.gca()
        self.axes.set_xlabel('Iterations')
        self.axes.set_ylabel('MSE for Price')
        self.axes.set_title("Mean Squared Error (MSE) for price")
        plt.xlim(self.xmin, self.xmax)
        plt.ylim(self.ymin, self.ymax)
        self.axes.set_xlim([self.xmin, self.xmax])
        self.axes.set_ylim([self.ymin, self.ymax])
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.get_tk_widget().grid(row=0, column=1)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row=0, column=0)

        self.plot_frame1 = tk.Frame(self.master)
        self.plot_frame1.grid(row=0, column=1)
        self.figure1 = plt.figure(figsize=figure_size)
        self.axes1 = self.figure1.gca()
        self.axes1.set_xlabel('Iterations')
        self.axes1.set_ylabel('MAE for Price')
        self.axes1.set_title("Mean Squared Error (MAE) for price")
        plt.xlim(self.xmin, self.xmax)
        plt.ylim(self.ymin, self.ymax)
        self.canvas1 = FigureCanvasTkAgg(self.figure1, master=self.plot_frame1)
        self.canvas1.get_tk_widget().grid(row=0, column=2)
        self.plot_widget1 = self.canvas1.get_tk_widget()
        self.plot_widget1.grid(row=0, column=2)

        # Slider frames
        self.frame_for_sliders = tk.Frame(self.master)
        self.frame_for_sliders.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.frame_for_sliders.rowconfigure(0, weight=1)
        self.frame_for_sliders.rowconfigure(1, weight=1)
        self.frame_for_sliders.rowconfigure(2, weight=1)
        self.frame_for_sliders.rowconfigure(3, weight=1)
        self.frame_for_sliders.rowconfigure(4, weight=1)
        self.frame_for_sliders.columnconfigure(0, weight=1, uniform='xx')

        # slider for Alpha (learning rate) : [range 0.001 and 1.0. Default value = 0.1]
        self.no_of_delayed_elements = tk.Scale(self.frame_for_sliders, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                               from_=0, to_=100, resolution=1, bg="#F1948A",
                                               activebackground="#FF0000",
                                               highlightcolor="#00FFFF",
                                               label="No. of Delayed Elements",
                                               command=lambda event: self.no_of_delayed_elements_callback())
        self.no_of_delayed_elements.set(10)
        self.no_of_delayed_elements.bind("<ButtonRelease-1>", lambda event: self.no_of_delayed_elements_callback())
        self.no_of_delayed_elements.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

        self.alpha_slider = tk.Scale(self.frame_for_sliders, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                     from_=0.001, to_=1.0, resolution=0.001, bg="#F1948A",
                                     activebackground="#FF0000",
                                     highlightcolor="#00FFFF",
                                     label="Learning Rate",
                                     command=lambda event: self.alpha_slider_callback())
        self.alpha_slider.set(0.1)
        self.alpha_slider.bind("<ButtonRelease-1>", lambda event: self.alpha_slider_callback())
        self.alpha_slider.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

        self.training_sample_size = tk.Scale(self.frame_for_sliders, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                             from_=0, to_=100, resolution=5, bg="#F1948A",
                                             activebackground="#FF0000",
                                             highlightcolor="#00FFFF",
                                             label="Training Sample Size",
                                             command=lambda event: self.training_sample_size_callback())
        self.training_sample_size.set(80)
        self.training_sample_size.bind("<ButtonRelease-1>", lambda event: self.training_sample_size_callback())
        self.training_sample_size.grid(row=2, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

        self.stride_value = tk.Scale(self.frame_for_sliders, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                               from_=1, to_=100, resolution=1, bg="#F1948A",
                               activebackground="#FF0000",
                               highlightcolor="#00FFFF",
                               label="Stride",
                               command=lambda event: self.stride_value_callback())
        self.stride_value.set(10)
        self.stride_value.bind("<ButtonRelease-1>", lambda event: self.stride_value_callback())
        self.stride_value.grid(row=3, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

        self.no_of_iterations = tk.Scale(self.frame_for_sliders, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                         from_=1, to_=100, resolution=1, bg="#F1948A",
                                         activebackground="#FF0000",
                                         highlightcolor="#00FFFF",
                                         label="No. of iterations",
                                         command=lambda event: self.no_of_iterations_callback())
        self.no_of_iterations.set(10)
        self.no_of_iterations.bind("<ButtonRelease-1>", lambda event: self.no_of_iterations_callback())
        self.no_of_iterations.grid(row=4, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

        # Buttons
        self.frame_for_buttons = tk.Frame(self.master)
        self.frame_for_buttons.grid(row=1, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self.frame_for_buttons.rowconfigure(0, weight=10)
        self.frame_for_buttons.rowconfigure(1, weight=10)
        self.frame_for_buttons.rowconfigure(2, weight=10)
        self.frame_for_buttons.columnconfigure(0, weight=1, uniform='xx')

        # Buttons for generating random weights and training
        self.set_weights_to_zero = tk.Button(self.frame_for_buttons, text="Set Weights to Zero",
                                             command=self.set_weights_to_zero_callback,
                                             bg="#85C1E9")
        self.set_weights_to_zero.grid(row=2, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)

        self.adjust_weight_direct_btn = tk.Button(self.frame_for_buttons, text="Adjust Weights (Direct)",
                                                  command=self.adjust_weight_direct_btn_callback, bg="#85C1E9")
        self.adjust_weight_direct_btn.grid(row=0, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)

        self.adjust_weight_lms_btn = tk.Button(self.frame_for_buttons, text="Adjust Weights (LMS)",
                                               command=self.adjust_weight_lms_btn_callback, bg="#C39BD3")
        self.adjust_weight_lms_btn.grid(row=1, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)

        # reading the files:
        self.dataset = self.read_csv_as_matrix(os.getcwd() + "\stock_data.csv")
        # normalizing the data:
        self.dataset = self.normalize_data(self.dataset)
        # set weights and bias to zero
        self.set_weights_to_zero_callback()
        # split data
        self.data_split()

        self.r = 2 * (self.delayed_elements + 1)
        self.total_me_lms = np.zeros((2, int(self.iterations)))
        self.total_me_direct = np.zeros((2, int(self.iterations)))

        for k in range(self.iterations):
            self.adjust_weights_lms(k)
        print("-----------------------------------------------")
        print("LMS Weights: ", self.weights)
        print("LMS MSE: ", self.total_me_lms[0:1, :])
        print("LMS MAE: ", self.total_me_lms[1:, :])
        print("-----------------------------------------------")

        for k in range(self.iterations):
            self.adjust_weights_direct(k)

        self.plot(self.total_me_direct[0:1, :], 1, 'mse', 'direct')

        self.plot(self.total_me_direct[1:, :], 2, 'mae', 'direct')
        self.plot(self.total_me_lms[0:1, :], 1, 'mse', 'lms')
        self.plot(self.total_me_lms[1:, :], 2, 'mae', 'lms')

        print("-----------------------------------------------")
        print("St pt Weights: ", self.weights)
        print("MSE: ", self.total_me_direct[0:1, :])
        print("MAE: ", self.total_me_direct[1:, :])
        print("-----------------------------------------------")

    def plot(self, y, figure_number, error, type):
        plt.figure(figure_number)
        plt.clf()
        x = np.arange(0, self.iterations, 1)
        if type == 'lms':
            color = 'green'
            if error == 'mse':
                label = "mse using lms"
                title = "MSE"
            else:
                label = "mae using lms"
                title = "MAE"
        else:
            color = 'red'
            if error == 'mse':
                label = "mse using direct"
                title = "MSE"
            else:
                label = "mae using direct"
                title = "MAE"

        plt.title(title + " for LMS & Direct")
        plt.xlabel('Iterations')
        plt.ylabel(title)
        plt.plot(x, np.transpose(y), color, label=label)
        plt.legend()
        plt.gcf().canvas.draw()

    def read_csv_as_matrix(self, file_name):
        # Each row of data in the file becomes a row in the matrix
        # So the resulting matrix has dimension [num_samples x sample_dimension]
        data = np.loadtxt(file_name, skiprows=1, delimiter=',', dtype=np.float32)
        return data

    def normalize_data(self, data):
        max_price = np.max(data[0:, 0])
        min_price = np.min(data[0:, 0])
        max_volume = np.max(data[0:, 1])
        min_volume = np.min(data[0:, 1])
        data[:, 0] = 2 * ((data[:, 0] - min_price) / (max_price - min_price)) - 1
        data[:, 1] = 2 * ((data[:, 1] - min_volume) / (max_volume - min_volume)) - 1
        return data

    def set_weights_to_zero_callback(self):
        self.weights = np.zeros((1, 2 * (self.delayed_elements + 1) + 1))
        self.weights[0][self.r - 1] = self.weights[0][self.r] = 1
        print("Weights and Bias set to zero!")
        print("Initial weights : ", self.weights)


    def train(self):
        training_size = int(self.training_samples.size / 2)
        for i in range(0, training_size, self.stride):
            j = i + self.delayed_elements + 1
            if j <= training_size - 1:
                target = self.training_samples[j][0].reshape(1, 1)
                input = self.vectorize_input(self.training_samples[i:j, :])
                a = np.dot(self.weights, np.transpose(input))
                error = target - a
                self.weights[:self.r - 1, :] = self.weights[:self.r - 1, :] + 2 * self.learning_rate * np.dot(error, input)
                self.weights[self.r:, :] = self.weights[self.r:, :] + np.dot(2 * self.learning_rate, error)

    def test(self, type, iter):
        testing_size = int(self.testing_samples.size / 2)
        total_mse = 0
        total_mae = 0
        for i in range(0, testing_size, self.stride):
            j = i + self.delayed_elements + 1
            if j <= testing_size - 1:
                target = self.testing_samples[j][0].reshape(1, 1)
                input = self.vectorize_input(self.testing_samples[i:j, :])
                a = np.dot(self.weights, np.transpose(input))
                total_mse += ((target - a)**2)
                total_mae += np.absolute(target - a)
        mse = total_mse / testing_size
        mae = total_mae / testing_size
        if type == 'lms':
            self.total_me_lms[0][iter] = mse
            self.total_me_lms[1][iter] = mae
        elif type == 'direct':
            self.total_me_direct[0][iter] = mse
            self.total_me_direct[1][iter] = mae

    def adjust_weight_lms_btn_callback(self):
        self.update_values()
        self.set_weights_to_zero_callback()
        self.data_split()
        for k in range(self.iterations):
            self.adjust_weights_lms(k)
        self.plot(self.total_me_lms[0:1, :], 1, 'mse', 'lms')
        self.plot(self.total_me_lms[1:, :], 2, 'mae', 'lms')
        print("-----------------------------------------------")
        print("LMS Weights: ", self.weights)
        print("LMS MSE: ", self.total_me_lms[0:1, :])
        print("LMS MAE: ", self.total_me_lms[1:, :])
        print("-----------------------------------------------")

    def adjust_weights_lms(self, iter):
        self.train()
        self.test('lms', iter)

    def adjust_weight_direct_btn_callback(self):
        print("Calculating stationary point:")
        self.update_values()
        self.set_weights_to_zero_callback()
        self.data_split()
        for k in range(int(self.iterations)):
            self.adjust_weights_direct(k)
        self.plot(self.total_me_direct[0:1, :], 1, 'mse', 'direct')
        self.plot(self.total_me_direct[1:, :], 2, 'mae', 'direct')
        print("-----------------------------------------------")
        print("St pt Weights: ", self.weights)
        print("MSE: ", self.total_me_direct[0:1, :])
        print("MAE: ", self.total_me_direct[1:, :])
        print("-----------------------------------------------")

    def adjust_weights_direct(self, iter):
        training_size = int(self.training_samples.size / 2)
        R = np.zeros((self.r + 1, self.r + 1))
        h = np.zeros((1, self.r + 1))

        for i in range(0, training_size, self.stride):
            j = i + self.delayed_elements + 1
            if j <= training_size - 1:
                input = self.vectorize_input(self.training_samples[i:j, :])
                target = self.training_samples[j][0].reshape(1, 1)
                R += np.dot(np.transpose(input), input)
                h += np.dot(target, input)
        R_inverse = inv(R)
        stationary_pt = np.transpose(np.dot(R_inverse, np.transpose(h)))
        self.weights = stationary_pt
        self.test('direct', iter)

    def data_split(self):
        eighty = int((self.dataset.size / 2) * (self.train_sample_size/100))
        self.training_samples, self.testing_samples = self.dataset[:eighty, :], self.dataset[eighty:, :]

    def vectorize_input(self, input):
        vector = np.zeros((1, self.r + 1))
        for i in range(self.delayed_elements + 1):
            vector[0][i] += input[i][0]
            vector[0][i + int(self.r / 2)] = input[i][1]
        vector[0][self.r] = 1
        return vector

    # The following three methods are Slider callback methods
    def alpha_slider_callback(self):
        self.update_values()
        self.learning_rate = self.alpha_slider.get()
        print("Updated  Learning Rate : ", self.learning_rate)

    # This method is the dropdown callback method
    def no_of_delayed_elements_callback(self):
        self.update_values()
        self.delayed_elements = self.no_of_delayed_elements.get()
        print("Updated No. of delayed elements : ", self.delayed_elements)

    def training_sample_size_callback(self):
        self.update_values()
        self.train_sample_size = self.training_sample_size.get()
        print("Updated Training sample size : ", self.train_sample_size)

    def stride_value_callback(self):
        self.update_values()
        self.stride = self.stride_value.get()
        print("Updated Stride : ", self.stride)

    # This method is the train callback method
    def no_of_iterations_callback(self):
        self.update_values()
        self.iterations = self.no_of_iterations.get()
        print("Updated No of iterations : ", self.iterations)

    def update_values(self):
        self.iterations = int(self.no_of_iterations.get())
        self.stride = int(self.stride_value.get())
        self.train_sample_size = int(self.training_sample_size.get())
        self.delayed_elements = int(self.no_of_delayed_elements.get())
        self.learning_rate = self.alpha_slider.get()
        self.r = 2 * (self.delayed_elements + 1)


main_window = MainWindow()
main_window.title('Kesavan_04_01: Widrow_Huff :  MSE and MAE')
main_window.mainloop()
