import imghdr
from flask import Flask,render_template,send_from_directory,abort,jsonify,request
import requests
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['API_KEY'] = "acc_a6910ab041ae060"
app.config['API_SECRET'] = "2cf42c857875adfcc4fbc3bfe72c3703"

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'images'

def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None        
    return '.' + (format if format != 'jpeg' else 'jpg')

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

@app.route('/uploadfiles' ,methods=["POST","GET"])
def uploadfiles():        
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)    
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        #if file_ext not in app.config['UPLOAD_EXTENSIONS'] or file_ext != validate_image(uploaded_file.stream):
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))    
        file_path = os.path.join(app.config['UPLOAD_PATH'] +"/" + filename)
        print(file_ext)        
    return jsonify(filepath="hohohoohhoh")

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/getobjectdetails/<path:url>')
def findobject(url):
    print(url)
    api_key = 'acc_a6910ab041ae060'
    api_secret = '2cf42c857875adfcc4fbc3bfe72c3703'
    image_url = 'https://i.picsum.photos/id/504/200/200.jpg?hmac=uNktbiKQMUD0MuwgQUxt7R2zjHBGFxyUSG3prhX0FWM'
    response = requests.get(
        'https://api.imagga.com/v2/tags?image_url=%s' % url,
        auth=(api_key, api_secret))
    return response.json()