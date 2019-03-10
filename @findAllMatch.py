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
import os


# export WERKZEUG_DEBUG_PIN=off


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
def upload_image():
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
    <title>Is this a picture of Expected?</title>
    <h1>Upload a picture and see if it's a picture of Expected!</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''


def findAllTrainingPicture():
    dirpath = os.getcwd()
    print("current directory is : " + dirpath)
    foldername = os.path.basename(dirpath)
    training_folder = dirpath + "/pictures"
    for item1, item2, item3 in os.walk(training_folder):
        print("item1", item1)
        print("item 2:", item2)
        print("item3", item3)
        return item3


def detect_faces_in_image(file_stream):
    sol_pic_dic = {"found": ""}
    picList = findAllTrainingPicture()
    print(picList, type(picList))

    face_found = False
    is_expected = False

    for picName in picList:
        picName = "pictures/" + picName
        print("8***********8 picName : ", picName)

        known_face_encoding = load_image_file(picName)
        # known_face_encoding_obama = load_image_file(picName_obama)
        known_face_encoding = known_face_encoding.tolist()

        img = face_recognition.load_image_file(file_stream)
        # Get face encodings for any faces in the uploaded image
        unknown_face_encodings = face_recognition.face_encodings(img)

        if len(unknown_face_encodings) > 0:
            face_found = True
            # See if the first face in the uploaded image matches the known face of Obama
            match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])
            if match_results[0]:
                is_expected = True
                sol_pic_dic["found"] += picName + ", "

                # Return the result as json
                result = {
                    "face_found_in_image": face_found,
                    "face_found_in_image_of": picName,
                    "is_picture_of_expected": is_expected
                }

                print("result : ", result)
                print(sol_pic_dic["found"])
                # return jsonify(result)
    if sol_pic_dic["found"]:
        return jsonify(sol_pic_dic)
    else:
        # if pic uploaded to test doesnt have face
        result = {
            "face_found_in_image": face_found
        }
        return jsonify(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
