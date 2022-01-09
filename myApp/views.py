from django.shortcuts import render
from django.contrib import messages
import joblib
import re
import trafilatura as tf
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Create your views here.
model = joblib.load('static/heading_model')
cv = joblib.load('static/count_vectorizer')
ps = PorterStemmer()

def heading_vector(heading):
    review = re.sub('[^a-zA-Z]',' ',heading)
    review = review.lower()
    review = review.split()
    review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
    review = ' '.join(review)
    review = cv.transform([review]).toarray()
    return review

def getPredictions(heading,url):
    if url!=''and heading=='':
        document = tf.fetch_url(url)
        doc_dict = tf.bare_extraction(document)
        url_heading = doc_dict['title']
        res = heading_vector(url_heading)
        return model.predict(res)
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
            result = getPredictions(description,url)
            if result == True:
                messages.success(request, 'True News')
                return render(request,'index.html')
            else:
                messages.info(request, 'Fake News')
                return render(request,'index.html')
        else:
            result = getPredictions(description,url)
            if result == True:
                messages.success(request, 'True News')
                return render(request,'index.html')
            else:
                messages.info(request, 'Fake News')
                return render(request,'index.html')
    return render(request,'index.html')
