# Main Web App Code

from flask import Flask, request, render_template, jsonify , redirect
from PIL import Image
import os
from AppData import aiCode,sendToWhat
import random as r
import threading
import configparser

app = Flask(__name__)
config = configparser.ConfigParser()
# Read the configuration file
config.read('config.ini')

# SERVER
HOST_ADDRESS = config.get("SERVER","HOST_IP") # Replace with actual IP
HOST_PORT = config.get("SERVER","HOST_PORT")
# WHATSAPP (Optional)
SEND_WHATSAPP_ALERT = config.getboolean("WHATSAPP","SEND_WHATSAPP_ALERT")
GROUP_ID = config.get("WHATSAPP","GROUP_ID")

# Directory to save uploaded images
UPLOAD_FOLDER = 'static/uploads/'
IMAGE_DATA_FOLDER = 'static/imageData/'

# Dictionary mapping animals to disturbing sound frequencies
animal_sound_frequencies = {
    'elephant': 270,
    'tiger': 12000,
    'crocodile': 10000,
    'boar': 1000,
    'bear' : 15000,
    'lion' : 10000,
    'human': 17000
    # Correct these values
}

_animal = None
_probability = None
_frequency = 0
_capturedImgPath = ''
_referenceImgPath = ''
_location = None

def reset_values(animal=None, probability=None, frequency=None, captured_image_path='', reference_image_path='',location=None):
    global _animal, _probability, _frequency, _capturedImgPath, _referenceImgPath,_location
    _animal = animal
    _probability = probability
    _frequency = frequency
    _capturedImgPath = captured_image_path
    _referenceImgPath = reference_image_path
    _location = location
 
@app.route('/')
def home():
    reset_values()
    return redirect("/index")

@app.route('/index')
def index():
    return render_template(
        'index.html', 
        animal=_animal, 
        probability=_probability, 
        frequency=_frequency, 
        captured_image_path=_capturedImgPath, 
        reference_image_path=_referenceImgPath,
        location = _location
    )

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
    probability = f"{(prediction[2]*100):.2f}"
    frequency = animal_sound_frequencies.get(fiveClassAnimal, 0)
    ref_file = f"{fiveClassAnimal}{r.randint(0, 2)}.jpg"
    reference_image_path = os.path.join(
            IMAGE_DATA_FOLDER, 
            "unidentified.png" if fiveClassAnimal == "unidentified" else ref_file
        )

    reset_values(
            animal.replace("_", " ") if fiveClassAnimal == "unidentified" else fiveClassAnimal,
            probability,
            frequency,
            captured_image_path.replace("static", ""),
            reference_image_path.replace("static", ""),
            f"{r.randint(0,9)}{chr(r.randint(65,90))}"
        )
    return redirect("/index",302)

def send_data():
    sendToWhat.send_to_group(GROUP_ID, _animal,f"static\\{_capturedImgPath}",_location)
    print("\nSent alert to whatsapp!")
    

@app.route('/receive', methods=['GET'])
def receive():
    if (SEND_WHATSAPP_ALERT):
        threading.Thread(target=send_data).start()
    print("\nSent data to drone!")
    return jsonify({
        'animal': _animal,
        'frequency': _frequency
    })

if __name__ == '__main__':
    app.run(host= HOST_ADDRESS, port=HOST_PORT)

