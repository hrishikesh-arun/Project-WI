# Web App Testing

import requests,random
#import urllib.request
from PIL import Image
import configparser

config = configparser.ConfigParser()
# Read the configuration file
config.read('config.ini')

# SERVER data from config.ini
HOST_ADDRESS = config.get("SERVER","HOST_IP")
HOST_PORT = config.get("SERVER","HOST_PORT")
server_url = f"http://{HOST_ADDRESS}:{HOST_PORT}"


file_path = "test\\"+input("Enter File Name (With extension): ")
# Placeholder image path
image_path = file_path
_dataReceived = False

def capture_and_send_image():
    with open(image_path, 'rb') as img_file:
        files = {'file': img_file}
        
        response = requests.post(server_url+"/upload", files=files)
        
        if response.status_code == 200 or response.status_code == 302:
            return True
        else:
            print(f"Error in POST request: {response.status_code} {response.text}")
            return False

def get_frequency():
    response = requests.get(server_url+"/receive")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data}")
        global _dataReceived
        _dataReceived = True
        return data.get("frequency", 0)
    else:
        print(f"Error in GET request: {response.status_code} {response.text}")
        return 0

def main_loop():
    while not _dataReceived:
        # Capture and send image
        if capture_and_send_image():
            # Get frequency from the server
            frequency = get_frequency()
            
            if frequency > 0:
                print(f"Playing frequency: {frequency} Hz")
            else:
                print("Frequency Data not given!! Playing Default Frequency!!")

if __name__ == "__main__":
    main_loop()
