import sounddevice as sd
import numpy as np

def callback(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10  # Adjust the multiplier for sensitivity

    if volume_norm > threshold:
        # Perform your desired action here, for example print a message
        print(f"Sound detected!                              {volume_norm}")
    else:
        print(f"                                             {volume_norm}")

# Set your desired threshold (adjust based on your environment)
threshold = 1  

# Set the sampling parameters
duration = 10  # in seconds
sample_rate = 44100  # typical audio sampling rate

# Start recording with the callback function
while True:
    with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate):
        sd.sleep(int(duration * 1000))
