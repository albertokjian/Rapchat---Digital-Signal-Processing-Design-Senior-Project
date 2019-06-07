# This is an attempt to modify time for each word
# By allocating a certain amount of time for each vowel and consonants

import os
import sys
from shutil import copy2
from big_phoney import BigPhoney
from timeStretch import timeStretch

phoney = BigPhoney()
# MS_PER_SYL = 273

tolerance = 50  # if segment is within x milliseconds from the normal speed
min_time = 120  # if segment is less than x milliseconds long
base_time = 20
ms_per_consonant = 40
ms_per_short_vowel = 100
ms_per_long_vowel = 240
CONSONANTS = ['B', 'CH', 'D', 'DH', 'DX', 'EL', 'EM', 'EN', 'F', 'G', 'HH', 'JH', 'K', 'L',
              'M', 'N', 'NG', 'NX', 'P', 'Q', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'WH',
              'Y', 'Z', 'ZH']
SHORT_VOWELS = ['AA', 'AE', 'AH', 'AO', 'AX', 'AXR', 'EH', 'IH', 'IX', 'UH']
LONG_VOWELS = ['AW', 'AY', 'ER', 'EY', 'IY', 'OW', 'OY', 'UW', 'UX']


# "$5.00" is pronounced "F AY1 V D AA1 L ER0 Z"
def timeEstimate(word):
    p = phoney.phonize(word)
    print(p)
    # remove digit and split into individual pronunciations
    ps = ''.join(i for i in p if not i.isdigit()).split()
    time = base_time
    for indv in ps:
        time += ms_per_consonant if indv in CONSONANTS else 0
        time += ms_per_short_vowel if indv in SHORT_VOWELS else 0
        time += ms_per_long_vowel if indv in LONG_VOWELS else 0
    return time


def modifySpeed(dir=".", speed_filename=""):
    out_dir = os.path.abspath(dir) + "_modified_speed"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    # print(out_dir)
    rates = []
    if speed_filename != "":
        with open(speed_filename) as g:
            for line in g:
                if line != '\n':
                    rates.append(line[-2])
        # Speed rates may be adjusted here
        for i in range(len(rates)):
            if rates[i] == 's':
                rates[i] = 0.9
            elif rates[i] == 'n':
                rates[i] = 1.1
            else:
                rates[i] = 1.5
        i = 0
    for file in os.listdir(dir):
        if file.endswith("wav"):
            info = os.path.splitext(file)[0].split('_')
            num = info[0]
            word = info[-3]
            start = int(info[-2])
            end = int(info[-1])
            # syl_count = phoney.count_syllables(word)
            # theoretical = syl_count * MS_PER_SYL
            theoretical = timeEstimate(word)
            if rates:
                theoretical /= rates[i]  # time / rate
                i += 1
            actual = end - start
            if abs(theoretical - actual) < tolerance or actual < min_time:
                print(num, word, theoretical, actual, 'no change')
                copy2(os.path.join(dir, file), os.path.join(out_dir, file))
            else:
                print(num, word, theoretical, actual,
                      'shrinked' if theoretical < actual else 'stretched')
                timeStretch(os.path.join(dir, file), os.path.join(
                    out_dir, file), actual/theoretical, 0)
    return out_dir


if __name__ == "__main__":
    # Usage: python $PYFILE ?[audio_chunk_dir] ?[speed_change_txt]
    if len(sys.argv) > 3:
        print('usage: %s ?[audio_chunk_dir] ?[speed_change_txt]' % sys.argv[0])
        sys.exit(1)
    audio_dir = "."
    if len(sys.argv) == 2:
        audio_dir = sys.argv[1]
        if not os.path.isdir(audio_dir):
            print('usage: %s ?[audio_chunk_dir]' % sys.argv[0])
            sys.exit(1)
        modifySpeed(audio_dir)
    if len(sys.argv) == 3:
        audio_dir = sys.argv[1]
        if not os.path.isdir(audio_dir):
            print('usage: %s ?[audio_chunk_dir]' % sys.argv[0])
            sys.exit(1)
        speed_filename = sys.argv[2]
        modifySpeed(audio_dir, speed_filename)
