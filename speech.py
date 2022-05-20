import azure.cognitiveservices.speech as speechsdk
import keys, http.client, urllib.request, urllib.parse, urllib.error, json, os, pymsgbox
import numpy as np
import PIL
from PIL import Image

audioFile = "audio_speech.wav"

SUBSCRIPTION_KEY = keys.subscription_key
SERVICE_REGION = keys.region

letters = keys.image_ref
keys.add_dict()

class SkipRiffHeaderAudioStream(speechsdk.audio.PullAudioInputStreamCallback):
    def __init__(self, filename: str):
        super().__init__()
        self._file = open(filename, "rb")
        self._file.seek(44)

    def read(self, buffer: memoryview) -> int:
        size = buffer.nbytes
        frames = self._file.read(size)
        buffer[:len(frames)] = frames
        return len(frames)

    def close(self) -> None:
        self._file.close()



def recognize_with_bad_header():
    speech_config = speechsdk.SpeechConfig(subscription=keys.subscription_key, region=keys.region)
    speech_config.speech_recognition_language = "en-US"

    audio_format = speechsdk.audio.AudioStreamFormat(44100, 16, 1)
    pull_stream_callback = SkipRiffHeaderAudioStream(audioFile)
    pull_stream = speechsdk.audio.PullAudioInputStream(stream_format=audio_format,
                                                       pull_stream_callback=pull_stream_callback)
    audio_config = speechsdk.AudioConfig(stream=pull_stream)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config, audio_config)

    result = speech_recognizer.recognize_once_async().get()

    return result.text


def retrieve_image():

    upper_list = []
    list_im = []

    list_im.clear()

    data = recognize_with_bad_header()
    transcript = list(''.join(data))

    upper_list = [x.upper() for x in transcript]

    tag_ids = []
    for each_alphabet in upper_list:
        tag = letters.get(each_alphabet)
        tag_ids.append(tag)


    for each_tag in tag_ids: 
        output_file = os.path.join("image",  str(each_tag) + '.jpg')

        list_im.append(output_file)


    try:
    
        imgs = [PIL.Image.open(i) for i in list_im]
        min_shape = sorted( [(np.sum(i.size), i.size) for i in imgs])[0][1]
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
        imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
                        
        imgs_comb = PIL.Image.fromarray(imgs_comb)
        imgs_comb.save('static/images/stitched_image.jpg')

        list_im.clear()
    except Exception as e:
        pymsgbox.alert('Unable to print image!')
        print("Error")


recognize_with_bad_header()
retrieve_image()

