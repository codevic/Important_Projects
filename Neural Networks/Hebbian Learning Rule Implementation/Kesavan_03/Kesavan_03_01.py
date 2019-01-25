# Kesavan, Kavya
# 1001-495-334
# 2018-07-10
# Assignment-03-01

import Kesavan_03_02 as dnat
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random as random
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.misc


class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.center_frame = tk.Frame(self)
        self.left_frame = Hebbian_Learning(self, self.center_frame)
        self.center_frame.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.center_frame.grid_propagate(True)
        self.center_frame.rowconfigure(1, weight=1, uniform='xx')
        self.center_frame.columnconfigure(0, weight=1, uniform='xx')
        self.center_frame.columnconfigure(1, weight=1, uniform='xx')
        self.left_frame.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)


class Hebbian_Learning(tk.Frame):
    def __init__(self, root, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.root = root
        # Variable declarations
        self.sample_filenames = []
        self.sample_images = np.array([])
        self.target_images = np.array([])
        self.sample_image_vector = np.array([])
        self.target_image_vector = []
        self.samples = np.array([])
        self.targets = np.array([])
        self.weights = np.array([])
        self.bias = np.array([])
        self.sample_training_set = np.array([])
        self.sample_test_set = np.array([])
        self.target_training_set = np.array([])
        self.target_test_set = np.array([])
        self.output = np.zeros((10, 200))
        self.hebbs_rule = "Delta Rule"  # "Filtered Learning" # "Unsupervised Hebb" #"Filtered Learning" #
        self.activation_function = "Linear"  # "Hyperbolic Tangent" # #"Symmetrical Hard limit"
        self.learning_rate = 0.1
        self.S = 1000
        self.error_matrix = np.zeros((1, 1000))
        self.confusion_matrix = np.array([])

        self.frame_for_plot = tk.Frame(self.master)
        self.frame_for_plot.grid(row=0, column=0, columnspan=4, sticky=tk.N + tk.E + tk.S + tk.W)
        self.frame_for_plot.rowconfigure(0, weight=1)
        self.frame_for_plot.columnconfigure(0, weight=1)
        self.figure = plt.figure("")
        self.axes = self.figure.gca()
        self.xmin = 0
        self.xmax = 1000
        self.ymin = 0
        self.ymax = 100
        plt.xlim(self.xmin, self.xmax)
        plt.ylim(self.ymin, self.ymax)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame_for_plot)

        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.frame_for_sliders = tk.Frame(self.master)
        self.frame_for_sliders.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.frame_for_sliders.rowconfigure(0, weight=1)
        self.frame_for_sliders.columnconfigure(0, weight=1, uniform='xx')

        # slider for Alpha (learning rate) : [range 0.001 and 1.0. Default value = 0.1]
        self.alpha_slider = tk.Scale(self.frame_for_sliders, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                     from_=0.001, to_=1.0, resolution=0.01, bg="#F1948A",
                                     activebackground="#FF0000",
                                     highlightcolor="#00FFFF",
                                     label="Alpha",
                                     command=lambda event: self.alpha_slider_callback())
        self.alpha_slider.set(0.1)
        self.alpha_slider.bind("<ButtonRelease-1>", lambda event: self.alpha_slider_callback())
        self.alpha_slider.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)

        # Buttons

        self.frame_for_buttons = tk.Frame(self.master)
        self.frame_for_buttons.grid(row=1, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self.frame_for_buttons.rowconfigure(0, weight=10)
        self.frame_for_buttons.rowconfigure(1, weight=10)
        self.frame_for_buttons.rowconfigure(2, weight=10)
        self.frame_for_buttons.columnconfigure(0, weight=1, uniform='xx')

        # Buttons for generating random weights and training

        self.adjust_weight_btn = tk.Button(self.frame_for_buttons, text="Adjust Weights (Learn)",
                                           command=self.learn_btn_callback, bg="#85C1E9")
        self.adjust_weight_btn.grid(row=0, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)

        self.create_random_weights_btn = tk.Button(self.frame_for_buttons, text="Randomize Weights",
                                                   command=self.create_random_weights_btn_callback, bg="#C39BD3")
        self.create_random_weights_btn.grid(row=1, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)

        self.confusion_matrix_btn = tk.Button(self.frame_for_buttons, text="Display Confusion Matrix", command=self.confusion_matrix_callback,
                                           bg="#85C1E9")
        self.confusion_matrix_btn.grid(row=2, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)

        # Frame for dropdown:
        self.frame_for_dropdowns = tk.Frame(self.master)
        self.frame_for_dropdowns.grid(row=1, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
        self.frame_for_dropdowns.rowconfigure(0, weight=10)
        self.frame_for_dropdowns.rowconfigure(1, weight=10)
        self.frame_for_dropdowns.columnconfigure(0, weight=1, uniform='xx')
        self.frame_for_dropdowns.columnconfigure(1, weight=1, uniform='xx')

        # Dropdown for activation function
        self.learning_rule_fn_label = tk.Label(self.frame_for_dropdowns, text="Select Learning Method:", justify="center",
                                               bg="#F8C471")
        self.learning_rule_fn_label.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.learning_rule_var = tk.StringVar()
        self.learning_rule_dropdown = tk.OptionMenu(self.frame_for_dropdowns, self.learning_rule_var,
                                                     "Filtered Learning", "Delta Rule", "Unsupervised Hebb",
                                                    command=lambda event: self.learning_rule_dropdown_callback())
        self.learning_rule_var.set("Delta Rule")
        self.learning_rule_dropdown.grid(row=0, column=1, sticky=tk.N + tk.E + tk.S + tk.W)

        self.activation_fn_label = tk.Label(self.frame_for_dropdowns, text="Activation Functions:", justify="center",
                                            bg="#F8C471")
        self.activation_fn_label.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.activation_fn_var = tk.StringVar()
        self.activation_fn_dropdown = tk.OptionMenu(self.frame_for_dropdowns, self.activation_fn_var,
                                                    "Symmetrical Hard limit", "Hyperbolic Tangent", "Linear",
                                                    command=lambda event: self.activation_fn_dropdown_callback())
        self.activation_fn_var.set("Linear")
        self.activation_fn_dropdown.grid(row=1, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
        # initialising weights and biases
        self.initialize_weights_and_bias()
        # reading from data and converting img to vector.
        self.image_to_vector()
        # Shuffle data
        self.shuffle_split_data(self.sample_images, self.target_images)
        # learn
        self.total_epochs = 1000
        self.learn(self.total_epochs)

    def shuffle_split_data(self, sample_images, target_images):
        shuffled_target = np.zeros((self.S, 10))
        shuffled_sample = np.zeros((self.S, 785))
        eighty = int(self.S * 0.8)
        indices = random.sample(range(0, self.S), self.S)
        i = -1
        for index in indices:
            i = i + 1
            shuffled_target[i] = target_images[index]
            shuffled_sample[i] = sample_images[index]
        self.targets = shuffled_target
        self.samples = shuffled_sample
        self.sample_training_set, self.sample_test_set = self.samples[:eighty, :], self.samples[eighty:, :]
        self.sample_training_set = np.transpose(self.sample_training_set)
        self.sample_test_set = np.transpose(self.sample_test_set)
        self.target_training_set, self.target_test_set = self.targets[:eighty, :], self.targets[eighty:, :]
        self.target_training_set = np.transpose(self.target_training_set)
        self.target_test_set = np.transpose(self.target_test_set)

        print("----------------------------------------------")
        print("Sample Train : ", self.sample_training_set.shape)
        print("Sample Test : ", self.sample_test_set.shape)
        print("----------------------------------------------")
        print("Target Train : ", self.target_training_set.shape)
        print("Target Test : ", self.target_test_set.shape)
        print("----------------------------------------------")


    def read_one_image_and_convert_to_vector(self, file_name):
        img = scipy.misc.imread(file_name).astype(np.float32)
        for i in range(len(img)):
            for j in range(len(np.transpose(img))):
                img[i][j] = (img[i][j] / 127.5) - 1.0
        return img.reshape(-1, 1)

    # Reads an image and converts it into vectors
    def image_to_vector(self):
        dir_path = os.getcwd()
        images_path = dir_path + "\Data"
        slash = "\\"

        self.sample_images = np.zeros((1000, 785))
        self.target_images = np.zeros((1000, 10))

        # Reading images as vectors
        count = -1
        for file in os.listdir(images_path):
            url = images_path + slash + file
            count = count + 1
            self.sample_image_vector = np.array(self.read_one_image_and_convert_to_vector(url))
            self.sample_filenames = np.append(self.sample_filenames, file)

            for i in range(len(self.sample_image_vector)):
                self.sample_images[count][i] = self.sample_image_vector[i]
        self.sample_images[:, -1] += 1

        # Creating Targets according to file names
        count = -1
        for file in os.listdir(images_path):
            count = count + 1;
            index = int(file[0])
            self.target_image_vector = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
            self.target_image_vector[index] = 1
            for i in range(len(self.target_image_vector)):
                self.target_images[count][i] = self.target_image_vector[i]
        """
        print("----------------------------------------------")
        print("Input matrix : ", self.sample_images.shape)
        print("----------------------------------------------")
        print("Target matrix : ", self.target_images.shape)
        print("----------------------------------------------")
        """

    def initialize_weights_and_bias(self):
        self.weights = np.random.uniform(-0.001, 0.001, (10, 785))
        """
        print("----------------------------------------------")
        print("Weights : ", self.weights.shape)
        print("----------------------------------------------")
        """

    def softmax(self, x):
        self.normalize(x)
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    def normalize(self, x):
        if np.isnan(x).any():
            return x/np.max(x)
        else:
            return x

    # This method calculates the net value for the different activation functions;
    def get_activation(self, net_value):
        net_value = self.normalize(net_value)
        if self.activation_function == "Linear":
            activation = net_value
        elif self.activation_function == "Symmetrical Hard limit":
            activation = net_value
            activation[activation >= 0] = 1.0
            activation[activation < 0] = -1.0
        elif self.activation_function == "Hyperbolic Tangent":
            activation = ((np.exp(net_value)) - (np.exp(-net_value))) / ((np.exp(net_value)) + (np.exp(-net_value)))
        activation = self.normalize(activation)
        activation = self.softmax(activation)
        max = np.argmax(activation)
        activation = np.empty(10)
        activation.fill(-1)
        activation = activation.reshape((1, 10))
        activation[0][max] = 1
        return activation

    def learn(self, epoch):
        self.output = np.zeros((10, 200))
        for e in range(0, epoch):
            if e % 100 == 0:
                print("Epoch - ", e, " :     ")
                #print("Weights: ", self.weights)
            for i in range(self.sample_training_set.shape[1]):
                self.train(i)
            error = 0
            for j in range(self.sample_test_set.shape[1]):
                error += self.test(j)
            error = float(error/self.sample_test_set.shape[1])*100
            self.error_matrix[0][e] += error
        self.error_matrix = self.error_matrix[:, :epoch]
        print("Error matrix: ")
        print(self.error_matrix)
        self.plot_errors(epoch)

    def train(self, i):
        input = self.sample_training_set[:, i]
        netvalue = np.dot(self.weights, input)
        output = self.get_activation(netvalue)
        target = self.target_training_set[:, i]
        # update weights using hebb's rule:
        self.update_weights_using_hebbs(input, target, output)

    def test(self, i):
        input = self.sample_test_set[:, i]
        netvalue = np.dot(self.weights, input)
        output = self.get_activation(netvalue).reshape((10, 1))
        target = self.target_test_set[:, i].reshape((10, 1))
        self.output[:, i] += output[:, 0]
        target_index = np.argmax(target)
        output_index = np.argmax(output)
        if target_index == output_index:
            return 0
        else:
            return 1

    def update_weights_using_hebbs(self, input, target, output):
        if self.hebbs_rule == "Filtered Learning":
            self.filtered_learning(input, target)
        elif self.hebbs_rule == "Delta Rule":
            self.delta_rule(input, output, target)
        elif self.hebbs_rule == "Unsupervised Hebb":
            self.unsupervised(input, output)
        self.weights = self.normalize(self.weights)

    # Hebb's variations
    def filtered_learning(self, input, target):
        target = target.reshape((10, 1))
        input = np.transpose(input.reshape((785, 1)))
        self.weights = ((1 - self.learning_rate) * self.weights) + (self.learning_rate * (np.dot(target, input)))

    def delta_rule(self, input, output, target):
        target = target.reshape((10, 1))
        output = output.reshape((10, 1))
        error = target - output
        input = np.transpose(input.reshape((785, 1)))
        self.weights = self.weights + (self.learning_rate * (np.dot(error, input)))

    def unsupervised(self, input, output):
        output = output.reshape((10, 1))
        input = np.transpose(input.reshape((785, 1)))
        self.weights = self.weights + (self.learning_rate * (np.dot(output, input)))

    # This method plots the graph
    def plot_errors(self, epoch):
        self.axes.cla()
        x = np.transpose(np.arange(epoch)).reshape((1, epoch))
        self.axes.plot(x, self.error_matrix, marker='o', markersize=2)
        self.canvas.draw()

    # The following two methods are the Button callback methods for creating random weights and training
    def create_random_weights_btn_callback(self):
        self.initialize_weights_and_bias()

    # The following three methods are Slider callback methods
    def alpha_slider_callback(self):
        self.learning_rate = self.alpha_slider.get()
        print("New Learning Rate : ", self.learning_rate)

    # This method is the dropdown callback method
    def learning_rule_dropdown_callback(self):
        self.hebbs_rule = self.learning_rule_var.get()
        print("New Hebbs Rule : ", self.hebbs_rule)

    def activation_fn_dropdown_callback(self):
        self.activation_function = self.activation_fn_var.get()
        print("New Activation Function : ", self.activation_function)

    # This method is the train callback method
    def learn_btn_callback(self):
        self.learn(100)

    def calc_confusion_matrix(self):
        target = self.target_test_set
        output = self.output
        confusion_matrix = np.zeros((target.shape[0], target.shape[0]))
        target_indexes = np.argmax(target, axis=0)
        #print(target_indexes)
        output_indexes = np.argmax(output, axis=0)
        #print(output_indexes)
        size = target_indexes.size
        for i in range(size):
            confusion_matrix[target_indexes[i]][output_indexes[i]] += 1
        return confusion_matrix

    def confusion_matrix_callback(self):
        print("Calculating Confusion Matrix...")
        self.confusion_matrix = self.calc_confusion_matrix()
        print("Confusion Matrix: ")
        print(self.confusion_matrix)
        dnat.display_numpy_array_as_table(self.confusion_matrix)
        err = 0
        for i in range(self.confusion_matrix.shape[0]):
            for j in range(self.confusion_matrix.shape[0]):
                if not (i == j):
                    err += self.confusion_matrix[i][j]
        print("Confusion Matrix Error : ", err)


main_window = MainWindow()
main_window.title('Kesavan_03_01: Error plotting')
main_window.mainloop()
