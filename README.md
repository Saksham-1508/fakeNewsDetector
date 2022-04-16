# fakeNewsDetector
 A Django based web app that uses a machine learning model to detect fake news
 Flow of work: 
 1. Enter the url of the viral image.
 2. Reverse image search is performed on the viral image.
 3. The urls where the image are scrapped for information from google.
 4. The important labels are passed to the fake news detection model.
 5. The model predicts whether the headlines associated with the image are fake or not.
 
<img width="1440" alt="Screen Shot 2022-04-16 at 1 35 33 PM" src="https://user-images.githubusercontent.com/84831188/163667468-31c76a34-00d9-437e-aa93-686d9dd9de82.png">
