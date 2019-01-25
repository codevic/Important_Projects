# Kesavan, Kavya
# 1001-495-334
# 2018-23-09
# Assignment-02-01

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random as random
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import matplotlib
matplotlib.use('TkAgg')


class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.center_frame = tk.Frame(self)
        self.left_frame = DecisionBoundaryForSingleNeuron(self, self.center_frame)
        self.center_frame.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.center_frame.grid_propagate(True)
        self.center_frame.rowconfigure(1, weight=1, uniform='xx')
        self.center_frame.columnconfigure(0, weight=1, uniform='xx')
        self.center_frame.columnconfigure(1, weight=1, uniform='xx')
        self.left_frame.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)


class DecisionBoundaryForSingleNeuron(tk.Frame):

    def __init__(self, root, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.root = root
        self.x_min, self.x_max = -10, 10
        self.y_min, self.y_max = -10, 10
        self.input_weight1, self.input_weight2 = 1, 1
        self.weight1, self.weight2, self.bias = self.input_weight1, self.input_weight2, 0
        self.target = [-1, -1, 1, 1]
        self.input, self.sample_input, self.weights, self.weights_plot = [], [], [], []
        self.activation_function = "Symmetrical Hard limit"
        self.frame_for_plot = tk.Frame(self.master)
        self.frame_for_plot.grid(row=0, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
        self.frame_for_plot.rowconfigure(0, weight=1)
        self.frame_for_plot.columnconfigure(0, weight=1)
        self.figure = plt.figure("")
        self.axes = self.figure.gca()
        self.axes.set_xlabel('Input')
        self.axes.set_ylabel('Output')
        self.axes.set_title("Decision Boundary")
        plt.xlim(self.x_min, self.x_max)
        plt.ylim(self.y_min, self.y_max)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame_for_plot)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.frame_for_sliders = tk.Frame(self.master)
        self.frame_for_sliders.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.frame_for_sliders.rowconfigure(0, weight=1)
        self.frame_for_sliders.rowconfigure(1, weight=1)
        self.frame_for_sliders.rowconfigure(2, weight=1)
        self.frame_for_sliders.columnconfigure(0, weight=1, uniform='xx')
        # slider for weight1
        self.weight1_slider = tk.Scale(self.frame_for_sliders, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                       from_=-10, to_=10, resolution=1, bg="#F1948A",
                                       activebackground="#FF0000",
                                       highlightcolor="#00FFFF",
                                       label="Weight 1",
                                       command=lambda event: self.weight1_slider_callback())
        self.weight1_slider.set(self.weight1)
        self.weight1_slider.bind("<ButtonRelease-1>", lambda event: self.weight1_slider_callback())
        self.weight1_slider.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        # slider for weight2
        self.weight2_slider = tk.Scale(self.frame_for_sliders, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                       from_=-10, to_=10, resolution=1, bg="#F1948A",
                                       activebackground="#FF0000",
                                       highlightcolor="#00FFFF",
                                       label="Weight 2",
                                       command=lambda event: self.weight2_slider_callback())
        self.weight2_slider.set(self.weight2)
        self.weight2_slider.bind("<ButtonRelease-1>", lambda event: self.weight2_slider_callback())
        self.weight2_slider.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        # slider for bias
        self.bias_slider = tk.Scale(self.frame_for_sliders, variable=tk.DoubleVar(), orient=tk.HORIZONTAL, from_=-10,
                                    to_=10, resolution=1, bg="#73C6B6", activebackground="#FF0000",
                                    highlightcolor="#00FFFF", label="Bias",
                                    command=lambda event: self.bias_slider_callback())
        self.bias_slider.set(self.bias)
        self.bias_slider.bind("<ButtonRelease-1>", lambda event: self.bias_slider_callback())
        self.bias_slider.grid(row=2, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

        self.frame_for_buttons = tk.Frame(self.master)
        self.frame_for_buttons.grid(row=1, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self.frame_for_buttons.rowconfigure(0, weight=10)
        self.frame_for_buttons.rowconfigure(1, weight=10)
        self.frame_for_buttons.columnconfigure(0, weight=1, uniform='xx')
        self.frame_for_buttons.columnconfigure(1, weight=1, uniform='xx')
        # Dropdown for activation function
        self.activation_fn_label = tk.Label(self.frame_for_buttons, text="Activation Functions:", justify="center",
                                            bg="#F8C471")
        self.activation_fn_label.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.activation_fn_var = tk.StringVar()
        self.activation_fn_dropdown = tk.OptionMenu(self.frame_for_buttons, self.activation_fn_var,
                                                    "Symmetrical Hard limit", "Hyperbolic Tangent", "Linear",
                                                    command=lambda event: self.activation_fn_dropdown_callback())
        self.activation_fn_var.set("Symmetrical Hard limit")
        self.activation_fn_dropdown.grid(row=0, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
        # Buttons for generating random weights and training
        self.create_random_weights_btn = tk.Button(self.frame_for_buttons, text="Generate Random Weights",
                                                   command=self.create_random_inputs_btn_callback, bg="#C39BD3")
        self.create_random_weights_btn.grid(row=1, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
        self.update_weight_btn = tk.Button(self.frame_for_buttons, text="Train", command=self.train_btn_callback,
                                           bg="#85C1E9")
        self.update_weight_btn.grid(row=2, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
        self.create_random_inputs_btn_callback()
        self.weight1 = self.weight1_slider.get()
        self.weight2 = self.weight2_slider.get()
        self.weights = np.array([self.weight1, self.weight2])
        self.weights = self.weights.reshape(2, 1)
        self.plot_decision_boundary()

    # This method calculates the weights and updates the graph
    def train(self):
        new_weight = self.weights
        for steps in range(0, 100):
            for index in range(0, len(self.sample_input)):
                net_value = self.bias + np.dot(self.sample_input[index], new_weight)
                actual_output = self.calculate_activation_fns(net_value)
                error = self.target[index] - actual_output
                """
                When using linear activation function the weights might explode.
                You need to use regularization on weights to make them small.
                Hence we check if the errors exceed and accordingly we reduce the error to regularize the new weights. 
                """
                if error > 1000 or error < -700:
                    error = error/10000
                sample_input = self.sample_input[index].reshape(2, 1)
                new_weight = new_weight + (error * sample_input)
                self.bias = self.bias + error
            self.weights_plot = new_weight
            self.input_weight1 = self.weights_plot[0]
            self.input_weight2 = self.weights_plot[1]
            self.weight1_slider.set(float(self.input_weight1[0]))
            self.weight2_slider.set(float(self.input_weight2[0]))
            self.bias_slider.set(self.bias)
            self.plot_decision_boundary()
        print("Inputs : ", self.input)
        print("Weight : ", self.weights_plot)
        print("Bias : ", self.bias)

    # This method calculates the net value for the different activation functions;
    def calculate_activation_fns(self, x):
        net_value = 0
        if self.activation_function == "Symmetrical Hard limit":
            if x >= 0:
                net_value = 1
            else:
                net_value = -1
        elif self.activation_function == "Hyperbolic Tangent":
            net_value = (math.exp(x) - math.exp(-x))/(math.exp(x) + math.exp(-x))
        elif self.activation_function == "Linear":
            net_value = x
        return net_value

    # This method plots the graph
    def plot_decision_boundary(self):
        self.axes.cla()
        plt.xlim(self.x_min, self.x_max)
        plt.ylim(self.y_min, self.y_max)
        plt.xlabel("x axis")
        plt.ylabel("y axis")
        plt.title('Decision Boundary for a single neuron with two inputs')
        self.axes.plot(self.input[0][:2], self.input[1][:2], 'bo')
        self.axes.plot(self.input[0][2:], self.input[1][2:], 'ys')
        self.canvas.draw()
        mesh_step_size = .1  # step size in the mesh
        x_min, x_max = self.x_min - 1, self.x_max + 1
        y_min, y_max = self.y_min - 1, self.y_max + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, mesh_step_size), np.arange(y_min, y_max, mesh_step_size))
        zz = self.input_weight1*xx + self.input_weight2*yy + self.bias
        cmp = mpl.colors.ListedColormap(['red', 'green'])
        zz[zz >= 0] = 1
        zz[zz < 0] = 0
        self.axes.pcolormesh(xx, yy, zz, cmap=cmp)
        self.canvas.draw()

    # The following two methods are the Button callback methods for creating random weights and training
    def create_random_inputs_btn_callback(self):
        temp_x = []
        temp_y = []
        for i in range(0, 4):
            x, y = random.randint(-10, 10), random.randint(-10, 10)
            temp_x.append(x)
            temp_y.append(y)
        self.input = np.array([temp_x, temp_y])
        self.sample_input = np.transpose(self.input)
        self.plot_decision_boundary()

    # The following three methods are Slider callback methods
    def weight1_slider_callback(self):
        self.weight1 = self.weight1_slider.get()
        self.plot_decision_boundary()

    def weight2_slider_callback(self):
        self.weight2 = self.weight2_slider.get()
        self.plot_decision_boundary()

    def bias_slider_callback(self):
        self.bias = self.bias_slider.get()
        self.plot_decision_boundary()

    # This method is the dropdown callback method
    def activation_fn_dropdown_callback(self):
        self.activation_function = self.activation_fn_var.get()
        self.plot_decision_boundary()

    # This method is the train callback method
    def train_btn_callback(self):
        self.train()


main_window = MainWindow()
main_window.title('Kesavan_02_01: Decision Boundary for a single neuron with two inputs')
main_window.mainloop()
