# Project WI - webTester
# v1.0
# Web App Testing

import requests,random

url = 'http://127.0.0.1:5000/upload'

# Path to the image file
image_path = f'test/test{random.randint(1,3)}.jpg'

# Open the image file
with open(image_path, 'rb') as img_file:
    files = {'file': img_file}
    
    # Send the image to the Flask server
    response = requests.post(url, files=files)
