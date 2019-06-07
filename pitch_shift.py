import wave
import numpy as np
from shutil import copy2

# import sys
# Code courtesy of Roland Smith:
# https://stackoverflow.com/questions/43963982/python-change-pitch-of-wav-file


def p_shift(filename, Hz, output):
    # Usage: python pitch_shift.py 'input.wav' 'frequency shift (Hz)'
    wr = wave.open(filename, 'r')
    # Set the parameters for the output file.
    par = list(wr.getparams())
    par[3] = 0  # The number of samples will be set by writeframes.
    par = tuple(par)
    ww = wave.open(output, 'w')
    ww.setparams(par)

    fr = 20
    sz = wr.getframerate()//fr  # Read and process 1/fr second at a time.
    # A larger number for fr means less reverb.
    c = int(wr.getnframes()/sz)  # count of the whole file
    shift = Hz//fr

    if c == 0:
        copy2(filename, output)
    else:
        for num in range(c):
            da = np.fromstring(wr.readframes(sz), dtype=np.int16)
            left, right = da[0::2], da[1::2]  # left and right channel
            lf, rf = np.fft.rfft(left), np.fft.rfft(right)
            lf, rf = np.roll(lf, shift), np.roll(rf, shift)
            # If shifting down in frequency, low frequencies get rolled
            # up to the highest ones, which is undesired
            # Therefore, we zero out the highest frequencies
            if shift < 0:
                lf[shift:0], rf[shift:0] = 0, 0
            # If shifting up in frequency, we zero the lowest frequencies
            else:
                lf[0:shift], rf[0:shift] = 0, 0
            nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
            ns = np.column_stack((nl, nr)).ravel().astype(np.int16)
            ww.writeframes(ns.tostring())
    ww.close()
    wr.close()