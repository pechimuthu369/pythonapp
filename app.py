import imghdr
import requests
import os
import json
from flask import Flask,render_template,send_from_directory,abort,jsonify,request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

import cv2
import sys



app = Flask(__name__,static_url_path="/static", static_folder="static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.debug = True

app.config['API_KEY'] = "acc_a6910ab041ae060"
app.config['API_SECRET'] = "2cf42c857875adfcc4fbc3bfe72c3703"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = "static/upload/"

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

@app.route('/facialfinder',methods=["POST","GET"])
def facialfinder():
    return render_template('facialfinder.html')

@app.route('/greet',methods=["POST","GET"])
def hello():
    return 'Hello, World!'

@app.route("/objectupload", methods=["GET", "POST"])
@cross_origin()
def ProcessImage():
    if request.method == "POST":        
        #print(request.files)
        try:
            if 'file' in request.files:
                uploaded_file = request.files['file']
                filename = secure_filename(uploaded_file.filename)    
                if filename != '':
                    file_ext = os.path.splitext(filename)[1]
                    if file_ext not in app.config['UPLOAD_EXTENSIONS'] or file_ext != validate_image(uploaded_file.stream):                    
                        abort(400)
                    file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
                    uploaded_file.save(file_path)     
                    image_abs_path = os.path.abspath(file_path)
                    #print(image_abs_path)  
                    response = requests.post(
                            'https://api.imagga.com/v2/tags',
                            auth=(app.config['API_KEY'], app.config['API_SECRET']),
                            files={'image': open(image_abs_path, 'rb')}).json()                                                                                                                                         
                    return response
        except Exception as e:
            print(e)            
        return jsonify("Ok")

@app.route("/facialupload", methods=["GET", "POST"])
@cross_origin()
def FacialImage():
    if request.method == "POST":                
        try:
            s = 0
            if len(sys.argv) > 1:
                s = sys.argv[1]

            source = cv2.VideoCapture(s)

            win_name = 'Camera Preview'
            cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

            net = cv2.dnn.readNetFromCaffe("deploy.prototxt",
                                        "res10_300x300_ssd_iter_140000_fp16.caffemodel")
            # Model parameters
            in_width = 300
            in_height = 300
            mean = [104, 117, 123]
            conf_threshold = 0.7

            while cv2.waitKey(1) != 27:
                has_frame, frame = source.read()
                if not has_frame:
                    break
                frame = cv2.flip(frame,1)
                frame_height = frame.shape[0]
                frame_width = frame.shape[1]

                # Create a 4D blob from a frame.
                blob = cv2.dnn.blobFromImage(frame, 1.0, (in_width, in_height), mean, swapRB = False, crop = False)
                # Run a model
                net.setInput(blob)
                detections = net.forward()

                for i in range(detections.shape[2]):
                    confidence = detections[0, 0, i, 2]
                    if confidence > conf_threshold:
                        x_left_bottom = int(detections[0, 0, i, 3] * frame_width)
                        y_left_bottom = int(detections[0, 0, i, 4] * frame_height)
                        x_right_top = int(detections[0, 0, i, 5] * frame_width)
                        y_right_top = int(detections[0, 0, i, 6] * frame_height)

                        cv2.rectangle(frame, (x_left_bottom, y_left_bottom), (x_right_top, y_right_top), (0, 255, 0))
                        label = "Confidence: %.4f" % confidence
                        label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                        cv2.rectangle(frame, (x_left_bottom, y_left_bottom - label_size[1]),
                                            (x_left_bottom + label_size[0], y_left_bottom + base_line),
                                            (255, 255, 255), cv2.FILLED)
                        cv2.putText(frame, label, (x_left_bottom, y_left_bottom),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

                t, _ = net.getPerfProfile()
                label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
                cv2.putText(frame, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
                cv2.imshow(win_name, frame)

                source.release()
                cv2.destroyWindow(win_name)
        except Exception as e:
            print(e)            
        return jsonify("Ok")

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