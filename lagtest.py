import sounddevice as sd
import numpy as np
import time
from multiprocessing import Process, Event
import sys
d=0
a=0
f=20000
for arg in sys.argv:
   
    if a==1:
        d=eval(arg)
        print(d)
        
    elif a==2:
        
        f=eval(arg)
        print(f)
    a=a+1

def play_tone(event, duration, frequency):
    start_time = time.time()
    t = np.arange(int(duration * 44100)) / 44100
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    sd.play(tone, samplerate=44100)
    sd.wait()
    end_time = time.time()
    event.set()  # Signal that the tone has been played
    print(end_time - start_time)
    return end_time - start_time

def listen_for_loud_sound(threshold_db, event):
    while True:
        audio_data = sd.rec(int(44100 * 0.1), samplerate=44100, channels=1)
        sd.wait()
        amplitude = np.max(np.abs(audio_data))
        if amplitude > threshold_db:
            event.set()  # Signal that the loud sound has been detected
            return amplitude

if __name__ == "__main__":
    # Set the threshold for loud sound (adjust as needed)
    loud_sound_threshold_db = 0.01

    # Create an event to synchronize between processes
    event = Event()

    print("Listening for a loud sound...")
    
    # Create a separate process for playing the tone
    tone_process = Process(target=play_tone, args=(event, d, f))
    tone_process.start()

    # Listen for the loud sound and measure the time
        #amplitude = listen_for_loud_sound(loud_sound_threshold_db, event)
    
    # Wait for the tone process to finish
    tone_process.join()

    # Loud sound detected, print the amplitude and the time taken in microseconds
        #print(f"Loud sound detected! Amplitude: {amplitude}")
        #print(f"Microphone lag time: {event.wait() * 1e6} microseconds")
