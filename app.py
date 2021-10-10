from flask import Flask,render_template,request

app = Flask(__name__)

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
