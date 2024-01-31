import sounddevice as sd
import numpy as np
import time
from multiprocessing import Process, Event
import sys

d = 0
f = 20000
a = 0

for arg in sys.argv:
    if a == 1:
        d = float(arg)
        print(f"Duration set to: {d} seconds")
    elif a == 2:
        f = float(arg)
        print(f"Frequency set to: {f} Hz")
    a += 1

def play_tone(event, duration, frequency):
    start_time = time.time()
    t = np.arange(int(duration * 44100)) / 44100
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    sd.play(tone, samplerate=44100)
    sd.wait()
    end_time = time.time()
    event.set()  # Signal that the tone has been played
    print(f"Tone played in {end_time - start_time} seconds")
    return end_time - start_time

def listen_for_loud_sound(threshold_db, event, target_frequency):
    while True:
        audio_data = sd.rec(int(44100 * 0.1), samplerate=44100, channels=1)
        sd.wait()
        amplitude = np.max(np.abs(audio_data))
        if amplitude > threshold_db:
            # Perform frequency analysis to check if the detected frequency is close to the target frequency
            frequencies, spectrum = np.fft.fftfreq(len(audio_data), d=1/44100), np.fft.fft(audio_data.flatten())
            dominant_frequency = frequencies[np.argmax(np.abs(spectrum))]
            
            # Set a threshold for frequency detection, adjust as needed
            frequency_threshold = 500  # Adjust this value based on your specific use case
            
            if abs(dominant_frequency - target_frequency) < frequency_threshold:
                event.set()  # Signal that the loud sound with the specified frequency has been detected
                return amplitude

if __name__ == "__main__":
    # Set the threshold for loud sound (adjust as needed)
    loud_sound_threshold_db = 0.01

    # Create an event to synchronize between processes
    event = Event()

    print("Listening for a loud sound with the specified frequency...")
    
    # Create a separate process for playing the tone
    tone_process = Process(target=play_tone, args=(event, d, f))
    tone_process.start()

    # Listen for the loud sound with the specified frequency and measure the time
    amplitude = listen_for_loud_sound(loud_sound_threshold_db, event, f)
    
    # Wait for the tone process to finish
    tone_process.join()

    # Loud sound detected, print the amplitude and the time taken in microseconds
    print(f"Loud sound with the specified frequency detected! Amplitude: {amplitude}")
    print(f"Microphone lag time: {event.wait() * 1e6} microseconds")
