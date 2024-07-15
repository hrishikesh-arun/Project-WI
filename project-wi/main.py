# Project WI
# v0.0.715.00
# Main Web App Code

from flask import Flask, request, jsonify, render_template
from PIL import Image
import io
import requests
from AppData import aiCode

app = Flask(__name__)

#### WORK TO BE DONE ####
# Dictionary mapping animals to disturbing sound frequencies
animal_sound_frequencies = {
    'cat': 15000,
    'dog': 12000,
    'bird': 18000,
    'elephant': 15
    # Add more animals and their disturbing frequencies
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    image = Image.open(io.BytesIO(file.read()))
    prediction = aiCode.identify_animal(image) # Identifies Animal
    animal = prediction[1]
    accuracy = float(prediction[2])
    frequency = animal_sound_frequencies.get(animal, 0)
    
    # Send frequency to ESP32
    esp_url = 'http://your_esp32_ip/receive'
    requests.post(esp_url, json={'frequency': frequency})

    return jsonify({
        'animal': animal,
        'accuracy': accuracy,
        'frequency': frequency
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

