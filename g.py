import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from .b import *
# Function to generate random data for the plot
def generate_data():
    return np.random.rand(100)

# Function to update the plot in real-time
def update_plot(frame):
    data = generate_data()
    line.set_ydata(data)
    ax.relim()
    ax.autoscale_view()
    return line,

# Create the main tkinter window
root = tk.Tk()
root.title("Real-time Matplotlib Plot")

# Create a Matplotlib figure and axis
fig, ax = plt.subplots()
x_data = np.arange(100)
y_data = generate_data()
line, = ax.plot(x_data, y_data, marker='o')

# Create a Tkinter canvas for the Matplotlib figure
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create a tkinter button to start the real-time update
start_button = ttk.Button(root, text="Start Update", command=lambda: ani.event_source.start())
start_button.pack(side=tk.LEFT, padx=10)

# Create a tkinter button to stop the real-time update
stop_button = ttk.Button(root, text="Stop Update", command=lambda: ani.event_source.stop())
stop_button.pack(side=tk.LEFT, padx=10)

# Use FuncAnimation to update the plot in real-time
ani = FuncAnimation(fig, update_plot, blit=True, interval=100)  # Update every 1000 milliseconds (1 second)

# Run the Tkinter main loop
root.mainloop()
