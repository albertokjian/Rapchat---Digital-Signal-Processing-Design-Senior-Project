import sys
import os
import json
from pydub import AudioSegment


def splitAudio(audio_file, transcript_file, dir=""):
    if (audio_file.lower().endswith('.wav')):
        audio = AudioSegment.from_wav(audio_file)
    if dir == "":
        dir = os.path.splitext(audio_file)[0] + "_audio_chunks"
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(transcript_file, 'r') as tf:
        lyrics = json.load(tf)
        i = 1
        for wts in lyrics:
            line = wts["string"]
            start = wts["start"]
            end = wts["end"]
            audio_chunk = audio[start:end]
            audio_chunk.export(os.path.join(dir, "{}_audio_chunk_{}_{}_{}.wav".format(
                i, line, round(start), round(end))), format='wav')
            i += 1


if __name__ == "__main__":
    # Usage: python $PYFILE [wav_file] [lyrics_json] [output_dir]
    if len(sys.argv) > 4 or len(sys.argv) < 3:
        print('usage: %s [wav_file] [lyrics_json] ?[output_dir]' % sys.argv[0])
        sys.exit(1)
        dir = "."
    if len(sys.argv) == 4:
        dir = sys.argv[3]
        if not os.path.isdir(dir):
            print(
                'usage: %s [wav_file] [lyrics_json] ?[output_dir]' % sys.argv[0])
            sys.exit(1)
    splitAudio(sys.argv[1], sys.argv[2])
