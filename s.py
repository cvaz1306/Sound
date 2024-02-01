import sounddevice as sd
import numpy as np

def callback(indata, frames, time, status):
    global prev_volume_norm

    volume_norm = np.linalg.norm(indata) * 10  # Adjust the multiplier for sensitivity

    if abs(volume_norm - prev_volume_norm) > sensitivity:
        # Perform your desired action here, for example print a message
        print(f"Sound level changed!  {volume_norm}")
    else:
        print(f"                      {volume_norm}")

    prev_volume_norm = volume_norm

# Set your desired sensitivity (adjust based on your environment)
sensitivity = 1

# Set the sampling parameters
sample_rate = 44100  # typical audio sampling rate

# Initialize previous volume level
prev_volume_norm = 0

# Start recording with the callback function
with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate):
    while True:
        sd.sleep(100)  # Sleep for a very long time (adjust as needed)
