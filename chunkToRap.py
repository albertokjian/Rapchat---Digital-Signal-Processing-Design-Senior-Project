import os
import sys
from modifySpeed import modifySpeed
from pitchAverager import pitchAverager
from normalizeLoudness import normalizeLoudness
from mergeToRap import mergeToRap


def chunkToRap(dir, txt):
    a = modifySpeed(dir, txt)
    b = pitchAverager(a)
    c = normalizeLoudness(b)
    d = mergeToRap(c, txt)
    print('See the rap file at {}'.format(d))


if __name__ == "__main__":
    # Usage: python $PYFILE [audio_chunk_dir] [speed_change_txt]
    if len(sys.argv) < 2:
        print('usage: %s [audio_chunk_dir] [speed_change_txt]' % sys.argv[0])
        sys.exit(1)
    audio_dir = sys.argv[1]
    if not os.path.isdir(audio_dir):
        print('usage: %s ?[audio_chunk_dir] [speed_change_txt]' % sys.argv[0])
        sys.exit(1)
    speed_filename = sys.argv[2]
    chunkToRap(audio_dir, speed_filename)
