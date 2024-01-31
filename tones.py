import sounddevice as sd
import numpy as np
import time
from multiprocessing import Process, Event
import sys

d = 0
frequencies = []
phases = []
a = 0

for arg in sys.argv:
    if a == 1:
        d = float(arg)
        print(f"Duration set to: {d} seconds")
    elif a > 1:
        # Extracting frequencies and phases from command line arguments
        frequency, phase = map(float, arg.split(':'))
        frequencies.append(frequency)
        phases.append(phase)
    a += 1

def play_tone(event, duration, frequencies, phases):
    start_time = time.time()
    t = np.arange(int(duration * 44100)) / 44100
    tones = [
        (0.5 * np.sin(2 * np.pi * frequency * t + np.radians(phase)))
        for frequency, phase in zip(frequencies, phases)
    ]
    tone=np.sum(tones)
    
    sd.play(tone, samplerate=44100)
    sd.wait()
    end_time = time.time()
    event.set()  # Signal that the tone has been played
    print(f"Tone played in {end_time - start_time} seconds")
    return end_time - start_time

if __name__ == "__main__":
    # Set the threshold for loud sound (adjust as needed)
    loud_sound_threshold_db = 0.01

    # Create an event to synchronize between processes
    event = Event()

    print("Listening for a loud sound with the specified frequency...")

    # Create a separate process for playing the tone
    tone_process = Process(target=play_tone, args=(event, d, frequencies, phases))
    tone_process.start()

    # Listen for the loud sound with the specified frequency and measure the time

    # Wait for the tone process to finish
    tone_process.join()
