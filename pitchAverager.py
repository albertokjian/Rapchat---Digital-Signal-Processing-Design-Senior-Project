import pitch_detect as pd
import pitch_shift as ps
import os
import sys
from shutil import copy2


tolerance = 30  # if segment is within x Hz from the average pitch
min_time = 120  # if segment is less than x milliseconds long


def pitchAverager(dir="."):
    out_dir = os.path.abspath(dir) + "_averaged_pitch"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # The folder where all the audio chunks are stored
    sum_pitch = 0
    count_pitch = 0
    pitch = {}
    excludeFiles = []
    for file in os.listdir(dir):
        if file.endswith("wav"):
            info = os.path.splitext(file)[0].split('_')
            num = info[0]
            start = int(info[-2])
            end = int(info[-1])
            if end - start < min_time:
                copy2(os.path.join(dir, file), os.path.join(out_dir, file))
                excludeFiles.append(file)
            else:
                pitch[num] = pd.get_pitch(os.path.join(dir, file))
                sum_pitch += pitch[num]
                count_pitch += 1

    avg_pitch = sum_pitch / count_pitch

    for file in os.listdir(dir):
        if file.endswith("wav") and file not in excludeFiles:
            inputfile = os.path.join(dir, file)
            outputfile = os.path.join(out_dir, file)
            info = os.path.splitext(file)[0].split('_')
            num = info[0]
            word = info[-3]
            print(word, pitch[num])
            Hz = int(avg_pitch - pitch[num])
            if Hz < tolerance:
                copy2(os.path.join(dir, file), os.path.join(out_dir, file))
            else:
                ps.p_shift(inputfile, Hz, outputfile)
    return out_dir


if __name__ == "__main__":
    # Usage: python $PYFILE ?[audio_chunk_dir]
    if len(sys.argv) > 2:
        print('usage: %s ?[audio_chunk_dir]' % sys.argv[0])
        sys.exit(1)
    audio_dir = "."
    if len(sys.argv) == 2:
        audio_dir = sys.argv[1]
        if not os.path.isdir(audio_dir):
            print('usage: %s ?[audio_chunk_dir]' % sys.argv[0])
            sys.exit(1)
        pitchAverager(audio_dir)
