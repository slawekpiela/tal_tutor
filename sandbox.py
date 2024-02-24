import sounddevice as sd
devs=sd.query_devices()
recording = sd.rec(int(4 * 44100), samplerate=44100, channels=2)
print(devs)
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

# Parameters
fs = 44100  # Sample rate
duration = 5  # Duration of recording in seconds
filename = 'output.wav'  # Filename to save the recording

print("Recording...")

# Record audio
recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')
sd.wait()  # Wait until recording is finished

print("Recording stopped. Saving...")

# Save the recording
write(filename, fs, recording)

print(f"File saved as {filename}")
