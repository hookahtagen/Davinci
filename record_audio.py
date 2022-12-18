import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

RATE = 44100
DURATION = 3

record = sd.rec(DURATION * RATE, samplerate=RATE, channels=2,dtype='float64')
print("RECORDING!\n")
sd.wait()
print("RECORDING COMPLETE! PLAYING NOW!")
sd.play(record, RATE)
sd.wait()
