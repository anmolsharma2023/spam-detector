
#from demosite.wsgi import main as app
#-Xfrozen_modules=off
#YDEVD_DISABLE_FILE_VALIDATION=1
from flask import Flask,render_template,request
import pickle
import string
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
app=Flask(__name__)


tfidf = pickle.load(open(r'C:\Users\Haha CORPORATION\Desktop\spamu\spammer\vectorizer.pkl','rb'))
model = pickle.load(open(r'C:\Users\Haha CORPORATION\Desktop\spamu\spammer\model.pkl','rb'))
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


@app.route('/', methods=["POST","GET"])
def home():
    if request.method=="POST":
        input=dict(request.form)
        transformed_sms = transform_text(input['shr'])
    
        vector_input = tfidf.transform([transformed_sms])
        
        result = model.predict(vector_input)[0]
        
        if result == 1:
            u="Spam"
        else:
            u="Not Spam"
        return render_template("index.html",out=u)
        
    return  render_template("index.html")

if __name__ == '__main__' :
    app.run(debug=True)