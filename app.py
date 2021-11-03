from flask import Flask,render_template,request
import requests
app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"


@app.route('/',methods=["POST","GET"])
def index():
    return render_template('weatherfinder.html')

@app.route('/weatherfinder',methods=["POST","GET"])
def weatherfinder():    
    return render_template('weatherfinder.html')

@app.route('/objectfinder',methods=["POST","GET"])
def objectfinder():
    return render_template('objectfinder.html')

@app.route('/greet',methods=["POST","GET"])
def hello():
    return 'Hello, World!'

@app.route('/findobject/<path:url>')
def findobject(url):
    print(url)
    api_key = 'acc_a6910ab041ae060'
    api_secret = '2cf42c857875adfcc4fbc3bfe72c3703'
    image_url = 'https://i.picsum.photos/id/504/200/200.jpg?hmac=uNktbiKQMUD0MuwgQUxt7R2zjHBGFxyUSG3prhX0FWM'
    response = requests.get(
        'https://api.imagga.com/v2/tags?image_url=%s' % url,
        auth=(api_key, api_secret))
    return response.json()