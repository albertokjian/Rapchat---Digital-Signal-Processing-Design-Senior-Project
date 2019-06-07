# Code from Python audio processing library 'aubio'
# https://github.com/aubio/aubio/blob/master/python/demos/demo_pitch.py
import sys
from aubio import source, pitch
import numpy as np


def get_pitch(filename):
    downsample = 1
    samplerate = 44100 // downsample
    # if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

    win_s = 4096 // downsample  # fft size
    hop_s = 512 // downsample  # hop size

    s = source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8

    pitch_o = pitch("schmitt", win_s, hop_s, samplerate)
    pitch_o.set_unit("Hz")
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        p = pitch_o(samples)[0]
        # pitch = int(round(p))
        confidence = pitch_o.get_confidence()
        # if confidence < 0.8: p = 0.
        # print("%f %f %f" % (total_frames / float(samplerate), p, confidence))
        pitches += [p]
        confidences += [confidence]
        total_frames += read
        if read < hop_s:
            break
    return np.mean(pitches)


if __name__ == "__main__":
    # Usage: python $PYFILE [wav]
    if len(sys.argv) < 1:
        print('usage: %s [wav]' % sys.argv[0])
        sys.exit(1)
    filename = sys.argv[1]
    print(get_pitch(filename))
