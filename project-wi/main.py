# Project WI
# v1.0
# Main Web App Code

from flask import Flask, request, render_template, url_for , redirect
from PIL import Image
import os
import requests
from AppData import aiCode
import random as r

app = Flask(__name__)

# Directory to save uploaded images
UPLOAD_FOLDER = 'static/uploads/'
IMAGE_DATA_FOLDER = 'static/imageData/'
DRONE_URL = '127.0.0.1:222523/recieve' # REPLACE WITH ACTUAL URL
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Dictionary mapping animals to disturbing sound frequencies
animal_sound_frequencies = {
    'elephant': 270,
    'tiger': 12000,
    'crocodile': 10000,
    'boar': 1000,
    'poachers': 17000
    # Add more animals and their disturbing frequencies
}

_animal = None
_accuracy = None
_frequency = None
_capturedImgPath = ''
_referenceImgPath = ''

def reset_values(animal=None,accuracy=None,frequency=None,captured_imagePath='', reference_imagePath=''):
    global _animal,_accuracy,_frequency,_capturedImgPath,_referenceImgPath
    _animal = animal
    _accuracy = accuracy
    _frequency = frequency
    _capturedImgPath = captured_imagePath
    _referenceImgPath = reference_imagePath
 
@app.route('/')
def home():
    reset_values()
    return redirect("/index")

@app.route('/index')
def index():
    return render_template('index.html', animal=_animal, accuracy=_accuracy, frequency=_frequency, captured_image_path=_capturedImgPath, reference_image_path = _referenceImgPath)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    # Save the uploaded image
    filename = file.filename
    captured_image_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(captured_image_path)
    
    image = Image.open(captured_image_path)
    prediction = aiCode.identify_animal(image)  # Identifies Animal
    animal = prediction[0]
    fiveClassAnimal = prediction[1]
    accuracy = f"{(prediction[2]*100):.2f}"
    frequency = animal_sound_frequencies.get(fiveClassAnimal, 10000)
    ref_file = fiveClassAnimal+f"{r.randint(0,2)}.jpg"
    reference_image_path = os.path.join(IMAGE_DATA_FOLDER, "unidentified.png" if fiveClassAnimal=="unidentified" else ref_file)
    print(reference_image_path)

    # Send frequency to ESP32
    try:
        requests.post(DRONE_URL, json={'frequency': frequency})
    except:
        print("Unable to send data to drone!!!")

    reset_values(animal.replace("_"," ") if fiveClassAnimal=="unidentified" else fiveClassAnimal,accuracy,"N/A" if fiveClassAnimal=="unidentified" else frequency,captured_image_path.replace("static",""),reference_image_path.replace("static",""))
    return redirect("/index",302)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=True)

