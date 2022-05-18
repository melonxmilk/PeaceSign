# flask
import os, pickle, pymsgbox, keys, time
from flask import Flask, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

# speech
from speech import recognize_with_bad_header, retrieve_image
from moviepy.editor import VideoFileClip
import azure.cognitiveservices.speech as speechsdk

# transcribe
import urllib.request, urllib.parse, urllib.error, cv2

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/speech', methods=['GET', 'POST'])
def speech():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
            return render_template('speech-transcription.html', request="POST")
    else:
            return render_template("speech.html")


@app.route('/speech-transcript', methods=['GET', 'POST'])
def speech_transcript():
    if recognize_with_bad_header() != "":
        recognized_text = recognize_with_bad_header()
        retrieve_image()
        return render_template("speech-transcription.html", recognized_text=recognized_text)
    else:
        pymsgbox.alert('Could not detect speech! Please try again!')
        return render_template("speech.html")


@app.route('/video', methods=['GET', 'POST'])
def video():
    return render_template('video.html')

@app.route('/video-transcript', methods=['GET', 'POST'])
def video_transcript():

    video = VideoFileClip("video.mp4")
    audio = video.audio
    audio.write_audiofile("audio.wav")
    subscription_key = keys.subscription_key
    speech_region = keys.region
    file_name = "audio.wav"

    def speech_recognize_continuous_from_file():

        speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=speech_region)
        audio_config = speechsdk.audio.AudioConfig(filename=file_name)

        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        done = False

        def stop_cb(evt):
            speech_recognizer.stop_continuous_recognition()
            nonlocal done
            done = True

        all_results = []
        def handle_final_result(evt):
            all_results.append(evt.result.text)

        speech_recognizer.recognized.connect(handle_final_result)
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        speech_recognizer.start_continuous_recognition()
        while not done:
            time.sleep(.5)

        with open("video/transcribed.pickle", "wb") as f:
            pickle.dump(all_results, f)
        
        return all_results

    concat_transcript = ' '.join(speech_recognize_continuous_from_file())

    def retrieve_video(): 
        letters = keys.image_ref
        keys.add_dict()


        upper_list = []
        list_im = []

        list_im.clear()

        data = pickle.load(open("video/transcribed.pickle", "rb"))
        transcript = list(' '.join(data))

        upper_list = [x.upper() for x in transcript]
        list_im = []

                    

        tag_ids = []
        for each_alphabet in upper_list:
            tag = letters.get(each_alphabet)
            tag_ids.append(tag)


        for each_tag in tag_ids: 
            output_file = os.path.join("image",  str(each_tag) + '.jpg')

            list_im.append(output_file)

        try:
            
            frames = [cv2.imread(i) for i in list_im]
            height, width, _ = frames[0].shape
            out = cv2.VideoWriter('static/images/output.avi', cv2.VideoWriter_fourcc(*'DIVX'), 3, (width, height))
            [out.write(f) for f in frames]
            out.release()

            list_im.clear()
            
        
        except Exception as e:
            pymsgbox.alert('Could not print video! Please try again!')
            pass
    
    
    retrieve_video()
    return render_template('video-transcript.html', concat_transcript=concat_transcript)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            f = request.files['file']
            f.save(secure_filename("video.mp4"))
        except Exception as e:
            pymsgbox.alert('No files detected, returning to interface.')
    return redirect(url_for('video_transcript'))


if __name__ == '__main__':
    app.run(threaded=True)