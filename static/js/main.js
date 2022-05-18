URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var pauseButton = document.getElementById("pauseButton");


recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);

function startRecording() {
	console.log("recordButton clicked");

    var constraints = { audio: true, video:false }

	recordButton.disabled = true;
	stopButton.disabled = false;
	pauseButton.disabled = false;
	submitButton.disabled = true;


	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		console.log("getUserMedia() success, stream created, initializing Recorder.js ...");


		audioContext = new AudioContext();

		gumStream = stream;

		input = audioContext.createMediaStreamSource(stream);


		rec = new Recorder(input,{numChannels:1})

		rec.record()

		console.log("Recording started");

	}).catch(function(err) {
    	recordButton.disabled = false;
    	stopButton.disabled = true;
    	pauseButton.disabled = true;
    	submitButton.disabled = true;

	});
}

function pauseRecording(){
	console.log("pauseButton clicked rec.recording=",rec.recording );
	if (rec.recording){
		rec.stop();
		pauseButton.innerHTML="Resume";
	}else{
		rec.record()
		pauseButton.innerHTML="Pause";

	}
}

function stopRecording() {
	console.log("stopButton clicked");

	stopButton.disabled = true;
	recordButton.disabled = true;
	pauseButton.disabled = true;
	submitButton.disabled = false;

	pauseButton.innerHTML="Pause";
	
	rec.stop();

	gumStream.getAudioTracks()[0].stop();

	rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {
	var url = URL.createObjectURL(blob);
	var au = document.createElement('audio');
	var li = document.createElement('li');
	var link = document.createElement('a');

	var filename = new Date().toISOString();

	au.controls = true;
	au.src = url;

	li.appendChild(au);
	li.appendChild(link);
	
	var upload = document.createElement('a');
	upload.href="#";
	// upload.innerHTML = "Upload";
	submitButton.addEventListener("click", function(event){
		  var xhr=new XMLHttpRequest();
		  xhr.onload=function(e) {
		      if(this.readyState === 4) {
		          console.log("Server returned: ",e.target.responseText);
		      }
		  };
		  var fd=new FormData();
		  fd.append("audio_data",blob, filename);
		  xhr.open("POST","/speech",true);
		  xhr.send(fd);
	})
	li.appendChild(upload)
	recordingsList.appendChild(li);
}

function updatePage() {
   window.location.reload();
    }


