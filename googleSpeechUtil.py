# set GOOGLE_APPLICATION_CREDENTIALS="XXXX.json"
import os
import json
credential_path = "XXXX.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
# def implicit():
#     from google.cloud import storage

#     # If you don't specify credentials when constructing the client, the
#     # client library will look for credentials in the environment.
#     storage_client = storage.Client()

#     # Make an authenticated API request
#     buckets = list(storage_client.list_buckets())
#     print(buckets)

# implicit()


def transcribe_gcs_with_word_time_offsets(gcs_uri):
    """Transcribe the given audio file asynchronously and output the word time
    offsets."""
    from google.cloud import speech
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        # encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        # sample_rate_hertz=44100,
        language_code='en-US',
        enable_word_time_offsets=True)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    result = operation.result(timeout=90)
    transcript = []

    filename = os.path.basename(gcs_uri)
    with open(os.path.splitext(filename)[0] + "_transcript.json", 'w') as output_file:
        for result in result.results:
            alternative = result.alternatives[0]
            print(u'Transcript: {}'.format(alternative.transcript))
            print('Confidence: {}'.format(alternative.confidence))

            for word_info in alternative.words:
                word = word_info.word
                start_time = round(
                    (word_info.start_time.seconds + word_info.start_time.nanos * 1e-9) * 1000)
                end_time = round(
                    (word_info.end_time.seconds + word_info.end_time.nanos * 1e-9) * 1000)
                print('Word: {}, start_time: {}, end_time: {}'.format(
                    word, start_time, end_time))
                transcript.append(
                    {"string": word, "start": start_time, "end": end_time})
        json.dump(transcript, output_file, indent=4)


transcribe_gcs_with_word_time_offsets(
    "gs://<container>/<wav_file>")
