# PeaceSign
Developed using Microsoft Azure's cognitive services and Flask framework as an initiative to aid the hearing-impaired for [Code Without Barriers](https://codewithoutbarriers.devpost.com/)'s hackathon, PeaceSign facilitates the translation of speech into sign language. After receiving user input, the application transcribes speech from short sentences and videos into hand signs.

<p align="center">
  <img width="250"  src="https://user-images.githubusercontent.com/58766039/171401680-1bda23d1-460f-43eb-9d80-3a0ef6bd3e87.png">
</p>

## Technologies
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) ![Azure](https://img.shields.io/badge/Microsoft_Azure-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white) &nbsp; ![Maintenance](http://unmaintained.tech/badge.svg)


⚠️ a/n: Solution will not work unless you replace all entries in keys.py with your own keypoints found on Azure Portal!

## Demo
![Audio Demo](https://user-images.githubusercontent.com/58766039/168831788-59d49e22-e661-4a48-8337-ae2b99a72cc9.gif)
![Video Demo](https://user-images.githubusercontent.com/58766039/167899593-868e5258-6b80-4be3-9945-bdf8b5d9092d.gif)


## Process
From all the available problem statements presented to participants within the hackathon, I went with whatever was the most socially beneficial issue to tackle just to fulfill my aspirations of creating solutions that enhance the quality of living for those who may require more assistance. With heavy reference to [Devbook](https://themes.3rdwavemedia.com/bootstrap-templates/startup/devbook-free-bootstrap-5-book-ebook-landing-page-template-for-developers/) template, I was able to effectively allocate more time to solution research and development instead of fiddling with the frontend.

The application's flow starts from the moment it receives a user input, where it transcribe speech into text. With the help of this [article](https://medium.com/nerd-for-tech/transcribe-audio-from-video-with-azure-cognitive-services-a4589a12d74f), I enhanced the capabilities of this project by forcing the model to receive continuous speech inputs for translation of hours long videos. For each alphabet in the transcription, the model fires an HTTP request from the API to retrieve images from the classifier trained with customvision.ai before dumping the results as a downloadable image.

⚠️ a/n: functions relating to customvision.ai were removed in major update (#1), please check previous versions for API request references

## Challenges
* **Time limitations:**
Participating in a hackathon enforces your disclipline to manage time effectively while being exposed to real-world problems. However, for someone who struggles with time management coupled with the lack of expertise in software development, having a time limit imposed upon was simply a fly in the ointment.
* **Resource:**
Having yet to reach the minimium required age to apply for credit card, I was unable to attain $200 Azure free trial credits for building this project. Fortunately, I was given $100 credits for a student account, but that also put me in a disadvantage as it would meant that the planned features had to reduce so I could save some credits for later use.
* **Bottlenecks:**
(this section has been fully updated, hopefully the application runs faster)
Functions in this project took at least 30mins to execute because an HTTP request was fired for every letter in the transcription. However, I believe there are easier ways to speed up the application e.g. threaded codes, classes
* **Incompatibility:**
Various python modules posed a huge problem in the project deployment to cloud as Azure web service only offers Linux containers for python e.g. pywin32, opencv

There are plans to migrate this project onto android platform for portability in the future, though still in consideration as I am in the process of learning Java. It was a very exciting and fruitful topic to conduct research on.

## How to use
To clone and run this application, you will need Git:
```
$ git clone https://github.com/melonxmilk/PeaceSign

# create virtual env
py -m venv .venv
.venv\scripts\activate


# install dependencies
$ pip install -r requirements.txt

# add the subcription key in keys.py

# run the application
$ flask run
```

A huge thanks to [Kerismaker Studio](https://iconscout.com/contributors/kerismaker) for their stunning icons and to everyone that has supported the growth of this project! 