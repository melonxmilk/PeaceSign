# flask
import os, pickle, pymsgbox, keys, time
from flask import Flask, redirect, render_template, request, url_for, session
from werkzeug.utils import secure_filename

# model
from flask_sqlalchemy import SQLAlchemy
from forms import SignUpForm, LoginForm

# speech
from speech import recognize_with_bad_header, retrieve_image
from moviepy.editor import VideoFileClip
import azure.cognitiveservices.speech as speechsdk

# transcribe
import urllib.request, urllib.parse, urllib.error, cv2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ehe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Peace.db'

db = SQLAlchemy(app)

"""Model for Users."""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

db.create_all()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = User(full_name = form.full_name.data, email = form.email.data, password = form.password.data)
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("signup.html", form = form, message = "This Email already exists in the system! Please Login instead.")
        finally:
            db.session.close()
        return render_template("signup.html", message = "Successfully signed up")
    return render_template("signup.html", form = form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data, password = form.password.data).first()
        if user is None:
            return render_template("login.html", form = form, message = "Wrong Credentials. Please Try Again.")
        else:
            session['user'] = user.id
            return render_template("login.html", message = "Successfully Logged In!")
    return render_template("login.html", form = form)

@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('index'))
    
@app.route("/speech", methods=["GET", "POST"])
def speech():
    if request.method == "POST":
        f = request.files["audio_data"]
        with open("audio_speech.wav", "wb") as audio:
            f.save(audio)
            return render_template("speech-transcription.html", request="POST")
    else:
        return render_template("speech.html")


@app.route("/speech-transcript", methods=["GET", "POST"])
def speech_transcript():
    if recognize_with_bad_header() != "":
        recognized_text = recognize_with_bad_header()
        retrieve_image()
        return render_template(
            "speech-transcription.html", recognized_text=recognized_text
        )
    else:
        pymsgbox.alert("Could not detect speech! Please try again!")
        return render_template("speech.html")


@app.route("/video", methods=["GET", "POST"])
def video():
    return render_template("video.html")


@app.route("/video-transcript", methods=["GET", "POST"])
def video_transcript():

    video = VideoFileClip("video.mp4")
    audio = video.audio
    audio.write_audiofile("audio_video.wav")
    subscription_key = keys.subscription_key
    speech_region = keys.region
    file_name = "audio_video.wav"

    def speech_recognize_continuous_from_file():

        speech_config = speechsdk.SpeechConfig(
            subscription=subscription_key, region=speech_region
        )
        audio_config = speechsdk.audio.AudioConfig(filename=file_name)

        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, audio_config=audio_config
        )

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
            time.sleep(0.5)

        with open("video/transcribed.pickle", "wb") as f:
            pickle.dump(all_results, f)

        return all_results

    concat_transcript = " ".join(speech_recognize_continuous_from_file())

    def retrieve_video():
        letters = keys.image_ref
        keys.add_dict()

        upper_list = []
        list_im = []

        list_im.clear()

        data = pickle.load(open("video/transcribed.pickle", "rb"))
        transcript = list(" ".join(data))

        upper_list = [x.upper() for x in transcript]

        tag_ids = []
        for each_alphabet in upper_list:
            tag = letters.get(each_alphabet)
            tag_ids.append(tag)

        for each_tag in tag_ids:
            output_file = os.path.join("image", str(each_tag) + ".jpg")

            list_im.append(output_file)

        try:

            frames = [cv2.imread(i) for i in list_im]
            height, width, _ = frames[0].shape
            out = cv2.VideoWriter(
                "static/images/output.avi",
                cv2.VideoWriter_fourcc(*"DIVX"),
                3,
                (width, height),
            )
            [out.write(f) for f in frames]
            out.release()

            list_im.clear()

        except Exception as e:
            pymsgbox.alert("Could not print video! Please try again!")
            pass

    retrieve_video()
    return render_template("video-transcript.html", concat_transcript=concat_transcript)


@app.route("/uploader", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        try:
            f = request.files["file"]
            f.save(secure_filename("video.mp4"))
        except Exception as e:
            pymsgbox.alert("No files detected, returning to interface.")
    return redirect(url_for("video_transcript"))


@app.route("/realtime", methods=["GET", "POST"])
def realtime():
    # has yet to add anything because i do not know how to code
    return render_template("realtime-translate.html")


if __name__ == "__main__":
    app.run(threaded=True)
