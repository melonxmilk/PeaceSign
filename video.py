import glob
import os
import azure.cognitiveservices.speech as speechsdk
import time, pickle, PIL, http.client, urllib.request, urllib.parse, urllib.error, json, os, pymsgbox, keys
import numpy as np
from PIL import Image
from moviepy.editor import VideoFileClip
import cv2

video = VideoFileClip("video.mp4")
audio = video.audio
audio.write_audiofile("audio.wav")
subscription_key = keys.subscription_key
speech_region = keys.region

file_name = "audio.wav"

speech_config = speechsdk.SpeechConfig(subscription_key, speech_region)
audio_config = speechsdk.AudioConfig(filename=file_name)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config, audio_config)

done = False
results = list()


letters = keys.tags
keys.add_dict()


def video_transcription():
    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        print(f"CLOSING on {evt}")
        speech_recognizer.stop_continuous_recognition()
        global done
        done = True
        print(f"CLOSED on {evt}")

    def recognised(evt):
        """Callback to process a single transcription"""
        recognised_text = evt.result.text
        results.append(recognised_text)
        print(f"Audio transcription: '{recognised_text}'")

    speech_recognizer.recognized.connect(recognised)

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(0.5)

    with open("video/transcribed.pickle", "wb") as f:
        pickle.dump(results, f)
        print("Transcription dumped")


"""
the output image is too large, so i have disable this function for video
transcription but if i can find a way to put 10 images horizontally and 
stack it to avoid piling, will re enable translation to images again
"""


def retrieve_video():

    headers = {"Training-Key": "replace_with_your_own_key"}

    upper_list = []
    list_im = []

    data = pickle.load(open("video/transcribed.pickle", "rb"))
    concat_transcript = list(" ".join(data))

    for x in concat_transcript:
        upper_list.append(x.upper())

    tag_ids = []
    for each_alphabet in upper_list:
        tag = letters.get(each_alphabet)
        tag_ids.append(tag)

    for each_tag in tag_ids:
        params = urllib.parse.urlencode(
            {
                "take": "1",
                "Endpoint": keys.endpoint,
                "projectId": keys.project_id,
                "iterationId": keys.iterationId,
                "tagIds": each_tag,
            }
        )

        try:
            conn = http.client.HTTPSConnection(
                "cwb-cognitiveservices.cognitiveservices.azure.com"
            )
            conn.request(
                "GET",
                "/customvision/v3.3/training/projects/85ae3371-e249-486b-801f-c5aa9fba4553/images/tagged?%s"
                % params,
                "{body}",
                headers,
            )
            response = conn.getresponse()
            data = response.read()
            data_json = json.loads(data)

            for item in data_json:
                originalImageUri = item["originalImageUri"]
                tag_name = item["tags"][0]["tagName"]
                output_file = os.path.join("image", tag_name + ".jpg")
                urllib.request.urlretrieve(originalImageUri, output_file)

            conn.close()

            print(list_im)
            list_im.append(output_file)

        except Exception as e:
            print("Error")

    try:
        frames = [cv2.imread(i) for i in list_im]
        height, width, _ = frames[0].shape
        out = cv2.VideoWriter(
            "output.avi", cv2.VideoWriter_fourcc(*"DIVX"), 1, (width, height)
        )
        [out.write(f) for f in frames]
        out.release()

        list_im.clear()

    except Exception as e:
        pymsgbox.alert("Could not print video! Please try again!")
        print("Error")


retrieve_video()
