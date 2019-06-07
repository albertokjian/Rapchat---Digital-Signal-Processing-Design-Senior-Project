import os
import sys
from pydub import AudioSegment


silence = AudioSegment.silent(duration=400)


def mergeToRap(dir, filename):
    audioMap = {}  # number: AudioSegment
    wordMap = {}  # number: word
    for file in os.listdir(dir):
        if file.endswith("wav"):
            chunk = AudioSegment.from_wav(os.path.join(dir, file))
            info = os.path.splitext(file)[0].split('_')
            num = info[0]
            word = info[-3]
            audioMap[num] = chunk
            wordMap[num] = word
    with open(filename, 'r') as g:
        i = 1
        combined = []
        for line in g:
            if line != '\n':
                word = line.split()[0]
                if wordMap[str(i)] != word:
                    print("{} is not found at correct position".format(word))
                if not combined:  # first segment
                    combined = audioMap[str(i)]
                else:
                    combined = combined.append(audioMap[str(i)], crossfade=10)
                i += 1
            else:
                combined = combined.append(silence, crossfade=250)
    combined.export(os.path.basename(dir) + '.wav', format='wav')
    return os.path.basename(dir) + '.wav'


if __name__ == "__main__":
    # Usage: python $PYFILE [audio_chunk_dir] [lyrics_txt]
    if len(sys.argv) < 2:
        print('usage: %s [audio_chunk_dir] [lyrics_txt]' % sys.argv[0])
        sys.exit(1)
    mergeToRap(sys.argv[1], sys.argv[2])
