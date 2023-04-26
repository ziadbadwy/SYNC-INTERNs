import cv2
import numpy as np
from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
import base64
from flask_cors import CORS
from tensorflow.keras.models import load_model

#initializes Flask
app = Flask(__name__)
#set secret key
app.config['SECRET_KEY'] = 'secret!'
#allow cross-origin resource sharing (CORS) from any origin.
socketio = SocketIO(app, cors_allowed_origins="*")
#load model
model = load_model('D:/sync intern/tasks/task2/server/myyymodel.h5')

#////CORS Policy///////
#CORS(app)

#route at the root URL ('/')
@app.route('/')
def index():
    #testing
    response = jsonify({'message': 'Hello'})
    #response.headers.add('Access-Control-Allow-Origin', '*')
    return response

#define haarcascades for detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#test connection 
@socketio.on('connect')
def test_connect():
    print('Client connected')

#client emits an image event to the server through a Socket
@socketio.on('image')
def handle_image(data):
    # Decode image then convert to binary
    img = base64.b64decode(data.split(',')[1])
    #convert from binary to numpy
    npimg = np.frombuffer(img, dtype=np.uint8)
    #openCV image format
    frame = cv2.imdecode(npimg, 1)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Extract face from the frame
        face_region = frame[y:y+h, x:x+w]
        # Resize the detcted face to fit the input shape of the model -> 224,224
        resized_face_region = cv2.resize(face_region, (224, 224))
        # Normalize the pixel values
        normalized_face_region = resized_face_region / 255.0
        # Add batch dimension to the face region (None,224,224,3) -> 1
        input_face = np.expand_dims(normalized_face_region, axis=0)
        #predictions
        pred = model.predict(input_face)[0][0]

        #thresholding
        if pred > 0.5:
            #drawing green rectangle -> (R,G,B)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            #add text to the frame putText(frame, "YOUR_TEXT", POSITION , FONT_TYPE, FONT_SCALE, COLOR(r,g,b))
            cv2.putText(frame, "Mask", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            acc_pos2 = (x, y + h + 20)
            acc = 100-pred
            cv2.putText(frame,  str(pred), acc_pos2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        else:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "No Mask", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            acc_pos2 = (x, y + h + 20)
            cv2.putText(frame,  str(pred), acc_pos2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    # Encode image send back to client
    retval, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    #emit('response_back', 'format and encoding' + jpg_as_text)
    emit('response_back', 'data:image/jpeg;base64,' + jpg_as_text)

if __name__ == '__main__':
    socketio.run(app)
