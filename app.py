from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weatherfinder')
def weatherfinder():
    return render_template('weatherfinder.html')

@app.route('/objectfinder')
def objectfinder():
    return render_template('objectfinder.html')

@app.route('/greet')
def hello():
    return 'Hello, World!'
