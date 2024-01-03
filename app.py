# from flask import Flask, render_template, request
# import cv2
# import numpy as np

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload():
#     # Handle the uploaded photo here
#     uploaded_photo = request.files['photo']
#     stored_photo = cv2.imread('/home/neww/Downloads/image_matching_app/static/image/stored_photo.jpeg')

#     # Convert images to grayscale
#     gray_uploaded = cv2.cvtColor(cv2.imdecode(np.fromstring(uploaded_photo.read(), np.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2GRAY)
#     gray_stored = cv2.cvtColor(stored_photo, cv2.COLOR_BGR2GRAY)

#     # Use template matching for comparison
#     res = cv2.matchTemplate(gray_uploaded, gray_stored, cv2.TM_CCOEFF_NORMED)
#     similarity = res.max()

#     if similarity > 0.40:
#         return "The photo of Gandhi is original on the note."
#     else:
#         return render_template('video.html')

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, request
import cv2
import os
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Handle the uploaded photo here
    uploaded_photo = request.files['photo']

    # Read the image data from the file stream
    uploaded_data = uploaded_photo.read()

    # Convert images to grayscale
    gray_uploaded = cv2.cvtColor(cv2.imdecode(np.fromstring(uploaded_data, np.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2GRAY)

    # Specify the path to the folder containing stored photos
    stored_photos_folder = '/home/neww/Downloads/image_matching_app/static/image/'

    # Loop through all files in the folder
    for filename in os.listdir(stored_photos_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):  # Add more file extensions if needed
            stored_photo_path = os.path.join(stored_photos_folder, filename)
            stored_photo = cv2.imread(stored_photo_path)

            # Convert stored photo to grayscale
            gray_stored = cv2.cvtColor(stored_photo, cv2.COLOR_BGR2GRAY)

            # Resize images to a common size for template matching
            height, width = gray_stored.shape[:2]
            gray_uploaded_resized = cv2.resize(gray_uploaded, (width, height))

            # Use template matching for comparison
            res = cv2.matchTemplate(gray_uploaded_resized, gray_stored, cv2.TM_CCOEFF_NORMED)
            similarity = res.max()

            # Adjust the similarity threshold as needed
            if similarity > 0.40:
                return "The photo of Gandhiji is original on the note."

    # If no match is found with any stored photo
    return render_template('video.html')

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=False, host='0.0.0.0')