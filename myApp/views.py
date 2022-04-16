from django.shortcuts import render
from django.contrib import messages
import joblib
import re
import trafilatura as tf
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession

# Create your views here.
model = joblib.load('static/heading_model')
cv = joblib.load('static/count_vectorizer')
ps = PorterStemmer()



def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

# SCRAPPING GOOGLE SEARCH RESULTS AFTER MATCHING IMAGE
def scrape_google(query):
    SEARCH_URL = 'https://www.google.com/searchbyimage?hl=en-US&image_url='
    query = urllib.parse.quote_plus(query)
    response = get_source(SEARCH_URL + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links

def heading_vector(heading):
    review = re.sub('[^a-zA-Z]',' ',heading)
    review = review.lower()
    review = review.split()
    review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
    review = ' '.join(review)
    review = cv.transform([review]).toarray()
    return review

# PREDICTION USING ML MODEL USING PASSIVE AGGRESSIVE CLASSIFIER
def getPredictions(heading,url):
    if url!=''and heading=='':
        links = scrape_google(url)
        if len(links):
            document = tf.fetch_url(links[0])
            doc_dict = tf.bare_extraction(document)
            url_heading = doc_dict['title']
            res = heading_vector(url_heading)
            return (model.predict(res),links[0])
        else:
            return "Can not validate"
    else:
        heading = heading_vector(heading)
        return model.predict(heading)

        
def index (request):
    if request.method=="POST":
        description =  request.POST.get("desc")
        url= request.POST.get("url")
        if url=='' and description=='':
            messages.warning(request, 'Please enter news headline or url')
            return render(request,'index.html')
        elif url!=''and description=='':
            res_ = getPredictions(description,url)
            result,link = res_
            if result == True:
                messages.success(request, 'True News')
                return render(request,'index.html',{"link":link})
            else:
                messages.info(request, 'Fake News')
                return render(request,'index.html',{"link":link})
        else:
            result = getPredictions(description,url)
            if result == True:
                messages.success(request, 'True News')
                return render(request,'index.html')
            else:
                messages.info(request, 'Fake News')
                return render(request,'index.html')
    return render(request,'index.html')
