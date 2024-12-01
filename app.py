from flask import Flask, request, jsonify
import base64
import numpy as np
import cv2
import face_recognition

app = Flask(__name__)

# Load known face encodings and names
known_face_encodings = []  # List to hold known face encodings
known_face_names = []      # List to hold corresponding names

def load_known_faces():
    # Load known faces and their encodings
    image1 = face_recognition.load_image_file("path/to/your/known_person1.jpg")  # Replace with your image path
    encoding1 = face_recognition.face_encodings(image1)[0]
    known_face_encodings.append(encoding1)
    known_face_names.append("Person 1")  # Replace with the person's name

    image2 = face_recognition.load_image_file("path/to/your/known_person2.jpg")  # Another known person
    encoding2 = face_recognition.face_encodings(image2)[0]
    known_face_encodings.append(encoding2)
    known_face_names.append("Person 2")  # Replace with the person's name

# Call the function to load known faces
load_known_faces()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    image_data = data['image'].split(',')[1]  # Get the base64 string
    image_data = base64.b64decode(image_data)  # Decode the image
    np_img = np.frombuffer(image_data, np.uint8)  # Convert to numpy array
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)  # Decode image

    # Convert the image from BGR to RGB
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Find all face encodings in the image
    face_encodings = face_recognition.face_encodings(rgb_img)

    if face_encodings:
        # Compare with known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encodings[0])
        name = "Unknown"

        # If a match is found, get the name
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Return success response with name or indicate unknown
        if name == "Unknown":
            return jsonify(success=False, message="Face not recognized.")
        else:
            return jsonify(success=True, name=name)
    else:
        return jsonify(success=False, message="No face detected.")

if __name__ == '__main__':
    app.run(debug=True)