# PeaceSign
Developed using Microsoft Azure's cognitive services and Flask framework as an initiative to aid the hearing-impaired for [Code Without Barriers](https://codewithoutbarriers.devpost.com/)'s hackathon, PeaceSign facilitates the translation of speech into American sign language. The web application can transcribe speech and convert both short sentences & video into hand signs after receiving speech input from the user.


<img src="static\images\hand-with-peace-symbol.png" alt="Alt text" style="float:right;" title="Optional title">

## Technologies
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)![Azure](https://img.shields.io/badge/Microsoft_Azure-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white)![Maintenance](http://unmaintained.tech/badge.svg)

note: upon deployment to GitHub, all data in keys.py are removed to prevent misuse. In order for the solution to work, you will be required to replace the entries with your own endpoints which can be found in your Azure's cognitive service.

## Process
From all the available problem statement presented in Code Without Barriers, I set down with what I believed to be the most socially beneficial problem statement to fulfill my aspirations of creating solutions that enhances the quality of living for people that needs it. With heavy reference to [Devbook](https://themes.3rdwavemedia.com/bootstrap-templates/startup/devbook-free-bootstrap-5-book-ebook-landing-page-template-for-developers/) template, I managed to reduce the required time for website design which allowed me to allocate more time for solution research & development.

To derive hand signs as an output, the model first transcribes speech into text, and with the help of this [article](https://medium.com/nerd-for-tech/transcribe-audio-from-video-with-azure-cognitive-services-a4589a12d74f), I was able to reach greater heights with the project and enhance the capabilities of the model to receive longer speech inputs from 30min videos after some minor adjustments to the source code. For each alphabet in the transcription, the model fires an HTTP request to get the images from the classifier trained in customvision.ai before dumping the results as a downloadable image.

**Challenges**
Due to time limitations imposed by the hackathon, along with my lack of expertise in software development, the planned features including real-time speech-to-sign translation and sign-to-speech was reduced to only short speech and video translation as I was running low on Azure credits with a starting amount of only a hundred on a student account. It was nonetheless, a very exciting and fruitful topic to conduct research on which can have produced good results if I had better time management.

Certain functions within this project take forever to load as an HTTP request is fired for each letter in the transcription, but I have managed to reduce the time taken from an hour to less than a minute. However, I still believe there are easier ways to speed up the application loading speed e.g. with class maybe. There are plans to migrate this project onto an android platform for portability in the future, though still in consideration as I am still in the process of learning and understanding Java language.

The incompatibility of python modules within PeaceSign also posed a huge problem in the deployment of the solution to the cloud as Azure Web only offers Linux containers for python and after several unsuccessful attempts of deployment, I managed to pin down the issue by running through the dependencies and singling out the modules that were causing container failures before replacing them with alternatives that perform the same functions.

## Demo
![Audio Demo](https://user-images.githubusercontent.com/58766039/168831788-59d49e22-e661-4a48-8337-ae2b99a72cc9.gif)
![Video Demo](https://user-images.githubusercontent.com/58766039/167899593-868e5258-6b80-4be3-9945-bdf8b5d9092d.gif)


## How to use
To clone and run this application, you will need Git
```
$ git clone https://github.com/melonxmilk/PeaceSign

# create virtual env
py -m venv .venv
.venv\scripts\activate


# install dependencies
$ pip install -r requirements.txt

# run the application
$ flask run
```
Similarly, you can access the cloud version [here](https://peacesign.azurewebsites.net/) on F0 tier (60 CPU minutes / day)

Congrats, your application is now up and running~ Now that you have read until this point, do consider supporting my work in the hackathon simply by voting on the project! Thank you :) A huge thanks to [Kerismaker Studio](https://iconscout.com/contributors/kerismaker) for their stunning icons used for PeaceSign!
