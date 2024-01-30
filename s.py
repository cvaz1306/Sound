import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def populate_array(starting_array, desired_length, value_to_add=0):
    result_array = starting_array.copy()
    while len(result_array) < desired_length:
        result_array = np.append(result_array, value_to_add)
    return result_array[:desired_length]

def callback(indata, frames, time, status):
    global prev_volume_norm, time_values, volume_values, ax

    volume_norm = np.linalg.norm(indata) * 10

    if abs(volume_norm - prev_volume_norm) > sensitivity:
        print(f"Sound level changed!  {volume_norm}")
    else:
        print(f"                      {volume_norm}")

    prev_volume_norm = volume_norm

    # Ensure time_values only contains numeric values
    if isinstance(time, (int, float)):
        time_values.append(time)
    else:
        time_values.append(0)  # Provide a default value if time is not numeric

    volume_values.append(volume_norm)

    # Update the x-axis limits to create a scrolling effect
    if time_values:
        ax.set_xlim(max(0, time_values[-window_size]), max(time_values) + 1)

    # Plot the difference graph
    ax.clear()
    ax.plot(time_values, populate_array(np.diff(volume_values), len(time_values), 0), color='b', marker='o')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Volume Difference')
    ax.set_title('Sound Level Difference Over Time')

sensitivity = 1.5
sample_rate = 44100
prev_volume_norm = 0
time_values = []
volume_values = []
window_size = 10  # Number of points to display in the window

fig, ax = plt.subplots()

with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate):
    ani = FuncAnimation(fig, callback, fargs=(None, None, None), interval=100, blit=False)
    plt.show()
