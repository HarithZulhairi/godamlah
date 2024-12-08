from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
import cv2
from datetime import date, datetime
import pandas as pd
import joblib
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# Defining Flask App
app = Flask(__name__)
app.secret_key = 'secret-key'  # Needed for session management and flash messages

nimgs = 10
datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")

# Initialize paths and create required directories
if not os.path.isdir('Attendance'):
    os.makedirs('Attendance')
if not os.path.isdir('static'):
    os.makedirs('static')
if not os.path.isdir('static/faces'):
    os.makedirs('static/faces')
if f'Attendance-{datetoday}.csv' not in os.listdir('Attendance'):
    with open(f'Attendance/Attendance-{datetoday}.csv', 'w') as f:
        f.write('Name,Roll,Time')

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Helper functions
def totalreg():
    return len(os.listdir('static/faces'))

def extract_faces(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_points = face_detector.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))
        return face_points
    except:
        return []

def identify_face(facearray):
    model = joblib.load('static/face_recognition_model.pkl')
    return model.predict(facearray)

def train_model():
    faces = []
    labels = []
    userlist = os.listdir('static/faces')
    for user in userlist:
        for imgname in os.listdir(f'static/faces/{user}'):
            img = cv2.imread(f'static/faces/{user}/{imgname}')
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)
    faces = np.array(faces)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces, labels)
    joblib.dump(knn, 'static/face_recognition_model.pkl')

def extract_attendance():
    df = pd.read_csv(f'Attendance/Attendance-{datetoday}.csv')
    return df['Name'], df['Roll'], df['Time'], len(df)

def add_attendance(name):
    username = name.split('_')[0]
    userid = name.split('_')[1]
    current_time = datetime.now().strftime("%H:%M:%S")
    df = pd.read_csv(f'Attendance/Attendance-{datetoday}.csv')
    if int(userid) not in list(df['Roll']):
        with open(f'Attendance/Attendance-{datetoday}.csv', 'a') as f:
            f.write(f'\n{username},{userid},{current_time}')

# Routing
@app.route('/')
def login_page():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Dummy credentials for demonstration purposes
    if email == 'test@example.com' and password == 'password123':
        # Capture a live image for face recognition
        video_capture = cv2.VideoCapture(0)
        ret, frame = video_capture.read()

        if not ret:
            flash('Unable to access webcam. Please try again.', 'danger')
            return redirect(url_for('login_page'))

        # Extract faces from the captured frame
        faces = extract_faces(frame)
        if len(faces) == 0:
            flash('No face detected. Please try again.', 'danger')
            video_capture.release()
            return redirect(url_for('login_page'))

        # Process each detected face for recognition
        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            resized_face = cv2.resize(face, (50, 50)).ravel().reshape(1, -1)
            try:
                # Identify the face using the pre-trained model
                identified_user = identify_face(resized_face)
                if identified_user:
                    session['logged_in'] = True
                    session['email'] = email
                    flash('Login successful!', 'success')
                    video_capture.release()
                    return redirect(url_for('home'))
            except Exception as e:
                flash(f'Error during face recognition: {e}', 'danger')

        video_capture.release()
        flash('Face recognition failed. Please try again.', 'danger')
        return redirect(url_for('login_page'))
    else:
        flash('Invalid email or password', 'danger')
        return redirect(url_for('login_page'))

@app.route('/home')
def home():
    if 'logged_in' not in session:
        return redirect(url_for('login_page'))
    names, rolls, times, l = extract_attendance()
    return render_template('home.html', names=names, rolls=rolls, times=times, l=l, totalreg=totalreg(), datetoday2=datetoday2)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
