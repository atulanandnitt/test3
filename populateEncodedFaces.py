# This is a _very simple_ example of a web service that recognizes faces in uploaded images.
# Upload an image file and it will check if the image contains a picture of Barack Obama.
# The result is returned as json. For example:
#
# $ curl -XPOST -F "file=@obama2.jpg" http://127.0.0.1:5001
#
# Returns:
#
# {
#  "face_found_in_image": true,
#  "is_picture_of_obama": true
# }
#
# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# NOTE: This example requires flask to be installed! You can install it with pip:
# $ pip3 install flask

import face_recognition
from flask import Flask, jsonify, request, redirect
import numpy as np
import PIL.Image
# export WERKZEUG_DEBUG_PIN=off

def storeEncodedFace(fileName, person_name, mode='RGB'):
    img = face_recognition.load_image_file(fileName)
    list_of_face_encodings = face_recognition.face_encodings(img)
    absolute_file = "encoded_faces/" + person_name
    with open(absolute_file,'w') as encodedFile:
        encodedFile.write(list_of_face_encodings)
    print("list_of_face_encodings", type(list_of_face_encodings))
    # return list_of_face_encodings[0]

def load_image_file(fileName, mode='RGB'):
    """
    Loads an image file (.jpg, .png, etc) into a numpy array

    :param fileName: image file name or file object to load
    :param mode: format to convert the image to. Only 'RGB' (8-bit RGB, 3 channels) and 'L' (black and white) are supported.
    :return: image contents as numpy array
    """
    # img = PIL.Image.open(file)
    img = face_recognition.load_image_file(fileName)
    list_of_face_encodings = face_recognition.face_encodings(img)
    return list_of_face_encodings[0]
    # if mode:
    #     im = im.convert(mode)
    # return np.array(im)


# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image_toTrain():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['picToTrain']
        person_name = request.files['nameOfThePerson']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            storeEncodedFace(file.filename, person_name)
            # The image file seems valid! Detect faces and return the result.
            return upload_image_toDetect()

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title> train and detect the person </title>
    <h1>Upload the picture to train</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="picToTrain">
      <input type="text" name="nameOfThePerson">
      <input type="submit" value="Upload">
    </form>
    '''



@app.route('/', methods=['GET', 'POST'])
def upload_image_toDetect():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <h1>Upload a picture and see if it's a picture of Expected!</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''

#
def detect_faces_in_image(file_stream):
    # Pre-calculated face encoding of Obama generated with face_recognition.face_encodings(img)

    picName_atul = "atul.JPG"
    # picName_obama = "obama.jpg"
    known_face_encoding_atul = load_image_file(picName_atul)
    # known_face_encoding_obama = load_image_file(picName_obama)
    known_face_encoding = known_face_encoding_atul.tolist()
    print('type(known_face_encoding) : ', type(known_face_encoding), known_face_encoding)
    # type(known_face_encoding) :  <class 'list'>
    print("*********************")
    print("compare obama encoding")
    # print(known_face_encoding_hardCoded == known_face_encoding_obama)
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)

    face_found = False
    is_obama = False

    if len(unknown_face_encodings) > 0:
        face_found = True
        # See if the first face in the uploaded image matches the known face of Obama
        print("known_face_encoding",  type(known_face_encoding))
        print("unknown_face_encodings[0]", type(unknown_face_encodings[0]))
        match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])
        if match_results[0]:
            is_obama = True

    # Return the result as json
    result = {
        "face_found_in_image": face_found,
        "is_picture_of_obama": is_obama
    }
    print("result : ", result)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
