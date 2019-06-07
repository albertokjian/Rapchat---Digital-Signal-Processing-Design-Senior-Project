import os
import sys
from pydub import AudioSegment
from shutil import copy2


def normalizeLoudness(dir="."):
    out_dir = os.path.abspath(dir) + "_normalized_loudness"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    print(out_dir)
    sum = 0
    count = 0
    excludeFiles = []
    for file in os.listdir(dir):
        if file.endswith("wav"):
            chunk = AudioSegment.from_wav(os.path.join(dir, file))
            loudness = chunk.dBFS
            if loudness == float('-inf'):
                copy2(os.path.join(dir, file), os.path.join(out_dir, file))
                excludeFiles.append(file)
            else:
                sum += loudness
                count += 1
                print(file, loudness)

    avg = sum / count * 1.1
    print(avg)
    for file in os.listdir(dir):
        if file.endswith("wav") and file not in excludeFiles:
            chunk = AudioSegment.from_wav(os.path.join(dir, file))
            loudness = chunk.dBFS
            normalized = chunk + (avg - loudness)
            normalized.export(os.path.join(out_dir, file), format='wav')
    return out_dir


if __name__ == "__main__":
    # Usage: python $PYFILE ?[audio_chunk_dir]
    if len(sys.argv) > 2:
        print('usage: %s ?[audio_chunk_dir]' % sys.argv[0])
        sys.exit(1)
    dir = "."
    if len(sys.argv) == 2:
        dir = sys.argv[1]
        if not os.path.isdir(dir):
            print('usage: %s ?[audio_chunk_dir]' % sys.argv[0])
            sys.exit(1)
    normalizeLoudness(dir)
