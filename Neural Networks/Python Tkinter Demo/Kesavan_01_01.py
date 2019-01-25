# Kesavan, Kavya
# 1001-495-334
# 2018-09-07
# Assignment-01-01
import Kesavan_01_02
import sys

if sys.version_info[0] < 3:
	import Tkinter as tk
else:
	import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
import matplotlib
from mpl_toolkits.mplot3d import Axes3D

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.backends.tkagg as tkagg


class MainWindow(tk.Tk):
	"""
	This class creates and controls the main window frames and widgets
	Kavya Kesavan 2018_09_07
	"""

	def __init__(self, debug_print_flag=False):
		tk.Tk.__init__(self)
		self.debug_print_flag = debug_print_flag
		self.master_frame = tk.Frame(self)
		self.master_frame.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
		self.rowconfigure(0, weight=1, minsize=500)
		self.columnconfigure(0, weight=1, minsize=500)
		# set the properties of the row and columns in the master frame
		# self.master_frame.rowconfigure(0, weight=1,uniform='xx')
		# self.master_frame.rowconfigure(1, weight=1, uniform='xx')
		self.master_frame.rowconfigure(2, weight=10, minsize=400, uniform='xx')
		self.master_frame.rowconfigure(3, weight=1, minsize=10, uniform='xx')
		self.master_frame.columnconfigure(0, weight=1, minsize=200, uniform='xx')
		#self.master_frame.columnconfigure(1, weight=1, minsize=200, uniform='xx')
		# create all the widgets
		self.menu_bar = MenuBar(self, self.master_frame, background='orange')
		#self.tool_bar = ToolBar(self, self.master_frame)
		self.left_frame = tk.Frame(self.master_frame)
		self.status_bar = StatusBar(self, self.master_frame, bd=1, relief=tk.SUNKEN)
		# Arrange the widgets
		self.menu_bar.grid(row=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
		#self.tool_bar.grid(row=1, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
		self.left_frame.grid(row=2, sticky=tk.N + tk.E + tk.S + tk.W)
		self.status_bar.grid(row=3, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
		# Create an object for plotting graphs in the left frame
		self.display_activation_functions = LeftFrame(self, self.left_frame, debug_print_flag=self.debug_print_flag)


class MenuBar(tk.Frame):
	def __init__(self, root, master, *args, **kwargs):
		tk.Frame.__init__(self, master, *args, **kwargs)
		self.root = root
		self.menu = tk.Menu(self.root)
		root.config(menu=self.menu)
		self.file_menu = tk.Menu(self.menu)
		self.menu.add_cascade(label="File", menu=self.file_menu)
		self.file_menu.add_command(label="New", command=self.menu_callback)
		self.file_menu.add_command(label="Open...", command=self.menu_callback)
		self.file_menu.add_separator()
		self.file_menu.add_command(label="Exit", command=self.menu_callback)
		self.dummy_menu = tk.Menu(self.menu)
		self.menu.add_cascade(label="Dummy", menu=self.dummy_menu)
		self.dummy_menu.add_command(label="Item1", command=self.menu_item1_callback)
		self.dummy_menu.add_command(label="Item2", command=self.menu_item2_callback)
		self.help_menu = tk.Menu(self.menu)
		self.menu.add_cascade(label="Help", menu=self.help_menu)
		self.help_menu.add_command(label="About...", command=self.menu_help_callback)

	def menu_callback(self):
		self.root.status_bar.set('%s', "called the menu callback!")

	def menu_help_callback(self):
		self.root.status_bar.set('%s', "called the help menu callback!")

	def menu_item1_callback(self):
		self.root.status_bar.set('%s', "called item1 callback!")

	def menu_item2_callback(self):
		self.root.status_bar.set('%s', "called item2 callback!")

class MyDialog(tk.simpledialog.Dialog):
	def body(self, parent):
		tk.Label(parent, text="Integer:").grid(row=0, sticky=tk.W)
		tk.Label(parent, text="Float:").grid(row=1, column=0, sticky=tk.W)
		tk.Label(parent, text="String:").grid(row=1, column=2, sticky=tk.W)
		self.e1 = tk.Entry(parent)
		self.e1.insert(0, 0)
		self.e2 = tk.Entry(parent)
		self.e2.insert(0, 4.2)
		self.e3 = tk.Entry(parent)
		self.e3.insert(0, 'Default text')
		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
		self.e3.grid(row=1, column=3)
		self.cb = tk.Checkbutton(parent, text="Hardcopy")
		self.cb.grid(row=3, columnspan=2, sticky=tk.W)

	def apply(self):
		try:
			first = int(self.e1.get())
			second = float(self.e2.get())
			third = self.e3.get()
			self.result = first, second, third
		except ValueError:
			tk.tkMessageBox.showwarning("Bad input", "Illegal values, please try again")


class StatusBar(tk.Frame):
	def __init__(self, root, master, *args, **kwargs):
		tk.Frame.__init__(self, master, *args, **kwargs)
		self.label = tk.Label(self)
		self.label.grid(row=0, sticky=tk.N + tk.E + tk.S + tk.W)

	def set(self, format, *args):
		self.label.config(text=format % args)
		self.label.update_idletasks()

	def clear(self):
		self.label.config(text="")
		self.label.update_idletasks()


class LeftFrame:
	"""
	This class creates and controls the widgets and figures in the left frame which
	are used to display the activation functions.
	Kavya Kesavan 2018_09_07
	"""

	def __init__(self, root, master, debug_print_flag=False):
		self.master = master
		self.root = root
		#########################################################################
		#  Set up the constants and default values
		#########################################################################
		self.xmin = -10
		self.xmax = 10
		self.ymin = -2
		self.ymax = 2
		self.input_weight = 1
		self.bias = 0.0
		self.activation_type = "Sigmoid"
		#########################################################################
		#  Set up the plotting frame and controls frame
		#########################################################################
		master.rowconfigure(0, weight=10, minsize=200)
		master.columnconfigure(0, weight=1)
		self.plot_frame = tk.Frame(self.master, borderwidth=10, relief=tk.SUNKEN)
		self.plot_frame.grid(row=0, column=0, columnspan=1, sticky=tk.N + tk.E + tk.S + tk.W)
		self.figure = plt.figure("")
		self.axes = self.figure.add_axes([0.15, 0.15, 0.6, 0.8])
		# self.axes = self.figure.add_axes()
		self.axes = self.figure.gca()
		self.axes.set_xlabel('Input')
		self.axes.set_ylabel('Output')
		# self.axes.margins(0.5)
		self.axes.set_title("")
		plt.xlim(self.xmin, self.xmax)
		plt.ylim(self.ymin, self.ymax)
		self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
		self.plot_widget = self.canvas.get_tk_widget()
		self.plot_widget.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
		self.plot_widget.pack(expand=1)
		# Create a frame to contain all the controls such as sliders, buttons, ...
		self.controls_frame = tk.Frame(self.master)
		self.controls_frame.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
		#########################################################################
		#  Set up the control widgets such as sliders and selection boxes
		#########################################################################
		self.input_weight_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
		                                    from_=-10.0, to_=10.0, resolution=0.01, bg="#DDDDDD",
		                                    activebackground="#FF0000", highlightcolor="#00FFFF", label="Input Weight",
		                                    command=lambda event: self.input_weight_slider_callback())
		self.input_weight_slider.set(self.input_weight)
		self.input_weight_slider.bind("<ButtonRelease-1>", lambda event: self.input_weight_slider_callback())
		self.input_weight_slider.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
		self.bias_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL, from_=-10.0,
		                            to_=10.0, resolution=0.01, bg="#DDDDDD", activebackground="#FF0000",
		                            highlightcolor="#00FFFF", label="Bias",
		                            command=lambda event: self.bias_slider_callback())
		self.bias_slider.set(self.bias)
		self.bias_slider.bind("<ButtonRelease-1>", lambda event: self.bias_slider_callback())
		self.bias_slider.grid(row=0, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
		#########################################################################
		#  Set up the frame for drop down selection
		#########################################################################
		self.label_for_activation_function = tk.Label(self.controls_frame, text="Activation Function Type:",
		                                              justify="center")
		self.label_for_activation_function.grid(row=0, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
		self.activation_function_variable = tk.StringVar()
		self.activation_function_dropdown = tk.OptionMenu(self.controls_frame, self.activation_function_variable,
		                                                  "Sigmoid", "Linear","Hyperbolic Tangent","Positive linear (RELU)", command=lambda
				event: self.activation_function_dropdown_callback())
		self.activation_function_variable.set("Sigmoid")
		self.activation_function_dropdown.grid(row=0, column=3, sticky=tk.N + tk.E + tk.S + tk.W)
		self.canvas.get_tk_widget().bind("<ButtonPress-1>", self.left_mouse_click_callback)
		self.canvas.get_tk_widget().bind("<ButtonPress-1>", self.left_mouse_click_callback)
		self.canvas.get_tk_widget().bind("<ButtonRelease-1>", self.left_mouse_release_callback)
		self.canvas.get_tk_widget().bind("<B1-Motion>", self.left_mouse_down_motion_callback)
		self.canvas.get_tk_widget().bind("<ButtonPress-3>", self.right_mouse_click_callback)
		self.canvas.get_tk_widget().bind("<ButtonRelease-3>", self.right_mouse_release_callback)
		self.canvas.get_tk_widget().bind("<B3-Motion>", self.right_mouse_down_motion_callback)
		self.canvas.get_tk_widget().bind("<Key>", self.key_pressed_callback)
		self.canvas.get_tk_widget().bind("<Up>", self.up_arrow_pressed_callback)
		self.canvas.get_tk_widget().bind("<Down>", self.down_arrow_pressed_callback)
		self.canvas.get_tk_widget().bind("<Right>", self.right_arrow_pressed_callback)
		self.canvas.get_tk_widget().bind("<Left>", self.left_arrow_pressed_callback)
		self.canvas.get_tk_widget().bind("<Shift-Up>", self.shift_up_arrow_pressed_callback)
		self.canvas.get_tk_widget().bind("<Shift-Down>", self.shift_down_arrow_pressed_callback)
		self.canvas.get_tk_widget().bind("<Shift-Right>", self.shift_right_arrow_pressed_callback)
		self.canvas.get_tk_widget().bind("<Shift-Left>", self.shift_left_arrow_pressed_callback)
		self.canvas.get_tk_widget().bind("f", self.f_key_pressed_callback)
		self.canvas.get_tk_widget().bind("b", self.b_key_pressed_callback)

	def key_pressed_callback(self, event):
		self.root.status_bar.set('%s', 'Key pressed')

	def up_arrow_pressed_callback(self, event):
		self.root.status_bar.set('%s', "Up arrow was pressed")

	def down_arrow_pressed_callback(self, event):
		self.root.status_bar.set('%s', "Down arrow was pressed")

	def right_arrow_pressed_callback(self, event):
		self.root.status_bar.set('%s', "Right arrow was pressed")

	def left_arrow_pressed_callback(self, event):
		self.root.status_bar.set('%s', "Left arrow was pressed")

	def shift_up_arrow_pressed_callback(self, event):
		self.root.status_bar.set('%s', "Shift up arrow was pressed")

	def shift_down_arrow_pressed_callback(self, event):
		self.root.status_bar.set('%s', "Shift down arrow was pressed")

	def shift_right_arrow_pressed_callback(self, event):
		self.root.status_bar.set('%s', "Shift right arrow was pressed")

	def shift_left_arrow_pressed_callback(self, event):
		self.root.status_bar.set('%s', "Shift left arrow was pressed")

	def f_key_pressed_callback(self, event):
		self.root.status_bar.set('%s', "f key was pressed")

	def b_key_pressed_callback(self, event):
		self.root.status_bar.set('%s', "b key was pressed")

	def left_mouse_click_callback(self, event):
		self.root.status_bar.set('%s', 'Left mouse button was clicked. ' + 'x=' + str(event.x) + '   y=' + str(
			event.y))
		self.x = event.x
		self.y = event.y
		self.canvas.focus_set()

	def left_mouse_release_callback(self, event):
		self.root.status_bar.set('%s',
		                         'Left mouse button was released. ' + 'x=' + str(event.x) + '   y=' + str(event.y))
		self.x = None
		self.y = None

	def left_mouse_down_motion_callback(self, event):
		self.root.status_bar.set('%s', 'Left mouse down motion. ' + 'x=' + str(event.x) + '   y=' + str(event.y))
		self.x = event.x
		self.y = event.y

	def right_mouse_click_callback(self, event):
		self.root.status_bar.set('%s', 'Right mouse down motion. ' + 'x=' + str(event.x) + '   y=' + str(event.y))
		self.x = event.x
		self.y = event.y

	def right_mouse_release_callback(self, event):
		self.root.status_bar.set('%s',
		                         'Right mouse button was released. ' + 'x=' + str(event.x) + '   y=' + str(event.y))
		self.x = None
		self.y = None

	def right_mouse_down_motion_callback(self, event):
		self.root.status_bar.set('%s', 'Right mouse down motion. ' + 'x=' + str(event.x) + '   y=' + str(event.y))
		self.x = event.x
		self.y = event.y

	def left_mouse_click_callback(self, event):
		self.root.status_bar.set('%s', 'Left mouse button was clicked. ' + 'x=' + str(event.x) + '   y=' + str(
			event.y))
		self.x = event.x
		self.y = event.y

	# self.focus_set()
	def display_activation_function(self):
		input_values = np.linspace(-10, 10, 256, endpoint=True)
		activation = Kesavan_01_02.calculate_activation_function(self.input_weight, self.bias, input_values,
		                                                          self.activation_type)
		self.axes.cla()
		self.axes.set_xlabel('Input')
		self.axes.set_ylabel('Output')
		self.axes.plot(input_values, activation)
		self.axes.xaxis.set_visible(True)
		plt.xlim(self.xmin, self.xmax)
		plt.ylim(self.ymin, self.ymax)
		plt.title(self.activation_type)
		self.canvas.draw()

	def input_weight_slider_callback(self):
		self.input_weight = np.float(self.input_weight_slider.get())
		self.display_activation_function()

	def bias_slider_callback(self):
		self.bias = np.float(self.bias_slider.get())
		self.display_activation_function()

	def activation_function_dropdown_callback(self):
		self.activation_type = self.activation_function_variable.get()
		self.display_activation_function()

def close_window_callback(root):
	if tk.messagebox.askokcancel("Quit", "Do you really wish to quit?"):
		root.destroy()


main_window = MainWindow(debug_print_flag=False)
# main_window.geometry("500x500")
main_window.wm_state('zoomed')
main_window.title('Assignment_01 --  Kesavan')
main_window.minsize(800, 600)
main_window.protocol("WM_DELETE_WINDOW", lambda root_window=main_window: close_window_callback(root_window))
main_window.mainloop()
