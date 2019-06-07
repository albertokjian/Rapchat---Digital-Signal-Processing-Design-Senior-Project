import sys
import json
import os
import re
from big_phoney import BigPhoney
phoney = BigPhoney()


# Check if two strings have a common substring
def checkForCommonSubstring(str1, str2):
    return sum(i == j for i in str1 for j in str2) > 0


def comparePhonetics(word1, word2):
    p1 = phoney.phonize(word1)
    p2 = phoney.phonize(word2)
    p1 = ''.join(i for i in p1 if not i.isdigit())
    p2 = ''.join(i for i in p2 if not i.isdigit())
    ps1 = p1.split()
    ps2 = p2.split()
    if len(ps1) != len(ps2):
        return False
    else:
        score = 0
        count = len(ps1)
        for i in range(count):
            if (ps1[i] == ps2[i]):  # give 1 score if perfect match
                score += 1
            # give 0.5 if partial match
            elif (checkForCommonSubstring(ps1[i], ps2[i])):
                score += 0.5
        return (score / count) > 0.5


def extractWordTimestamp(cmu_filename):
    with open(cmu_filename) as cf:
        transcript = []
        for x in cf:
            if re.findall(r"\s\d+\.\d+\s\d+\.\d+\s\d+\.\d+", x):
                tmp_arr = x.split()
                word = tmp_arr[0]
                start_time = round(float(tmp_arr[1]) * 1000)
                end_time = round(float(tmp_arr[2]) * 1000)
                if "<" not in word and word != "[NOISE]" and word != "[SPEECH]":
                    word = re.sub(r"\(.*\)", "", word)
                    print('Word: {}, start_time: {}, end_time: {}'.format(
                        word, start_time, end_time))
                    transcript.append(
                        {"string": word, "start": start_time, "end": end_time})
    # with open(os.path.splitext(cmu_filename)[0] + "_cmu_transcript.json", 'w') as of:
    #     json.dump(transcript, of, indent=4)

    return transcript


def updateTimestamp(google, cmu):
    transcript = []
    tol = 3  # start matching the next word if unmatched within 3 words
    il = 0  # last unmatched google index
    jl = 0  # last unmatched cmu index
    i = 0  # current google index
    j = 0  # current cmu index
    t = 0  # mismatch tolerance count
    flag = 0  # unresovled lines exist
    matched = 0  # matched ith word in google
    while(i < len(google)):
        g = google[i]
        print("google", i, il, g['string'])
        while (j < len(cmu) and t < tol and not matched):
            c = cmu[j]
            print("cmu", j, jl, c['string'])
            if (comparePhonetics(g['string'].lower(), c['string'].lower())):
                if flag:
                    id = i - il
                    jd = j - jl
                    if (id == 1 and jd == 0):  # out of nowhere word from google
                        g = google[il]
                        g['start'] = cmu[jl-1]['end']
                        g['end'] = cmu[jl]['start']
                        transcript.append(g)
                        il += 1
                        print(g, "out of nowhere")
                    elif (id == jd):  # match each word if the same number of words
                        while(il < i and jl < j):
                            g = google[il]
                            c = cmu[jl]
                            c['string'] = g['string']
                            transcript.append(c)
                            jl += 1
                            print(c, "same number of unmatched words")
                            il += 1
                    elif (id < jd and id == 1):  # only one mismatched word
                        g = google[il]
                        g['start'] = cmu[jl]['start']
                        g['end'] = cmu[j-1]['end']
                        transcript.append(g)
                        print(g, "only one mismatched word")
                    else:  # just use the cmu words instead
                        while(jl < j):
                            transcript.append(cmu[jl])
                            print(cmu[jl], "just use cmu")
                            jl += 1
                flag = 0
                t = 0
                il = i + 1
                jl = j + 1
                transcript.append(cmu[j])
                print(cmu[j], "perfect")
                matched = 1
                tol = 3
            else:
                flag = 1
                t += 1
            j += 1
        i += 1
        t = 0
        j = jl
        matched = 0
        tol += i - il
    print(transcript)
    return transcript


if __name__ == "__main__":
    # Usage: python $PYFILE [transcript_json] [cmuSphinx_transcript]
    # cmuSphinx transcript created using pocketsphinx_continuous -time yes
    if len(sys.argv) < 2:
        print(
            'usage: %s [transcript_json] [cmuSphinx_transcript]' % sys.argv[0])
        sys.exit(1)
    google_filename = sys.argv[1]
    cmu_filename = sys.argv[2]
    with open(google_filename) as jf:
        google_transcript = json.load(jf)
    cmu_transcript = extractWordTimestamp(cmu_filename)
    transcript = updateTimestamp(google_transcript, cmu_transcript)
    with open(os.path.splitext(google_filename)[0] + "_better.json", 'w') as of:
        json.dump(transcript, of, indent=4)
    with open(os.path.splitext(google_filename)[0] + "_better.txt", 'w') as of:
        for i in transcript:
            of.write("%s\n" % i['string'])
