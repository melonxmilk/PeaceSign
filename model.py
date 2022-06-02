"""
model.py was created and adjusted for flask usage but you may run this file alone to test
transcription of speech and sign language output in /model
"""

import azure.cognitiveservices.speech as speechsdk
import http.client, urllib.request, urllib.parse, urllib.error, json, os, pymsgbox, keys, time
import numpy as np
import PIL
from PIL import Image

letters = keys.image_ref
keys.add_dict()


def recognize_from_microphone():
    speech_config = speechsdk.SpeechConfig(
        subscription=keys.subscription_key, region=keys.region
    )
    speech_config.speech_recognition_language = "en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    print("Speak into your microphone.")

    result = speech_recognizer.recognize_once_async().get()

    print(result.text)

    return result.text


def retrieve_image():

    upper_list = []
    list_im = []

    list_im.clear()

    data = recognize_from_microphone()
    transcript = list("".join(data))

    upper_list = [x.upper() for x in transcript]

    tag_ids = []
    for each_alphabet in upper_list:
        tag = letters.get(each_alphabet)
        tag_ids.append(tag)

    for each_tag in tag_ids:
        output_file = os.path.join("image", str(each_tag) + ".jpg")

        list_im.append(output_file)

    try:

        imgs = [PIL.Image.open(i) for i in list_im]
        min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
        min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
        imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))

        imgs_comb = PIL.Image.fromarray(imgs_comb)
        imgs_comb.save("static/images/stitched_image.jpg")

        list_im.clear()
    except Exception as e:
        pymsgbox.alert("Unable to print image!")
        print("Error")


def speech_recognize_continuous():
    speech_config = speechsdk.SpeechConfig(
        subscription=keys.subscription_key, region=keys.region
    )
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    done = False

    def stop_cb(evt):
        nonlocal done
        done = True

    transcript = speech_recognizer.recognized.connect(
        lambda evt: print("{}".format(evt.result.text))
    )
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(0.5)

    speech_recognizer.stop_continuous_recognition()

