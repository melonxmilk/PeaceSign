'''
model.py was created and adjusted for flask usage but you may run this file alone to test
transcription of speech and sign language output in /model
'''

import azure.cognitiveservices.speech as speechsdk
import http.client, urllib.request, urllib.parse, urllib.error, json, os, pymsgbox, keys
import numpy as np
import PIL
from PIL import Image

letters = keys.tags
keys.add_dict()



def recognize_from_microphone():
    speech_config = speechsdk.SpeechConfig(subscription=keys.subscription_key, region=keys.region)
    speech_config.speech_recognition_language="en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")

    result = speech_recognizer.recognize_once_async().get()
    
    print(result.text)

    return result.text


def retrieve_image():

    headers = {
    'Training-Key': 'replace_with_your_own_key'
    }

    upper_list = []
    list_im = []

    for i in recognize_from_microphone():
        upper_list.append(i.upper())
        

    tag_ids = []
    for each_alphabet in upper_list:
        tag = letters.get(each_alphabet)
        tag_ids.append(tag)

    
    for each_tag in tag_ids:
        params = urllib.parse.urlencode({
            'take': '1',
            'Endpoint': keys.endpoint,
            'projectId': keys.project_id,
            'iterationId': keys.iterationId,
            'tagIds': each_tag
            })


        try:
                conn = http.client.HTTPSConnection(
            'cwb-cognitiveservices.cognitiveservices.azure.com')
                conn.request(
            "GET", "/customvision/v3.3/training/projects/85ae3371-e249-486b-801f-c5aa9fba4553/images/tagged?%s" % params, "{body}", headers)
                response = conn.getresponse()
                data = response.read()
                data_json = json.loads(data)


                for item in data_json:
                    originalImageUri = item['originalImageUri']
                    tag_name = item["tags"][0]["tagName"]
                    output_file = os.path.join("image",  tag_name + '.jpg')
                    urllib.request.urlretrieve(originalImageUri, output_file)
                    
                conn.close()

                list_im.append(output_file)
                

        except Exception as e:
            print("Error")

    try:
        imgs = [PIL.Image.open(i) for i in list_im]
        min_shape = sorted( [(np.sum(i.size), i.size) for i in imgs])[0][1]
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
        imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
                        
        imgs_comb = PIL.Image.fromarray(imgs_comb)
        imgs_comb.save('model/stitched_image.jpg')
        list_im.clear()
    except Exception as e:
        pymsgbox.alert('Could not print image! Please try again!')
        print("Error")


recognize_from_microphone
retrieve_image()