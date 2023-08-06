from time import sleep
import simpleaudio as sa
import numpy as np


def sound(beeps=3, seconds=0.75, seconds_between_beep=0.5):
    for _ in range(beeps):
        frequency = 440
        fs = 44100

        t = np.linspace(0, seconds, seconds * fs, False)
        note = np.sin(frequency * t * 2 * np.pi)
        audio = (note * (2 ** 15 - 1) / np.max(np.abs(note))).astype(np.int16)

        play_obj = sa.play_buffer(audio, 1, 2, fs)
        play_obj.wait_done()

        if beeps > 1:
            sleep(seconds_between_beep)
