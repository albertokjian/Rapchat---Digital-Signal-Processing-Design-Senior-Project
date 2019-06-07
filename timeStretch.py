import sys
from audiotsm import phasevocoder
from audiotsm.io.wav import WavReader, WavWriter


def timeStretch(input_filename, output_filename, rate, samplerate):
    with WavReader(input_filename) as reader:
        with WavWriter(output_filename, reader.channels, reader.samplerate) as writer:
            tsm = phasevocoder(reader.channels, rate)
            tsm.run(reader, writer)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: {:s} <input_filename> <output_filename> <rate> [samplerate]".format(
            sys.argv[0]))
        print("""Examples:
        # twice faster
        {0} track_01.mp3 track_01_faster.wav 2.0
        # twice slower
        {0} track_02.flac track_02_slower.wav 0.5
        # one and a half time faster, resampling first the input to 22050
        {0} track_02.flac track_02_slower.wav 1.5 22050""".format(sys.argv[0]))
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    rate = float(sys.argv[3])

    samplerate = 0 if len(sys.argv) < 5 else int(sys.argv[4])
    timeStretch(input_filename, output_filename, rate)
