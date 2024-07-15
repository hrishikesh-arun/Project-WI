# Project WI - AppData.aiCode
# v0.0.715.00-00
# Contains the Identifier AI

import tensorflow as tf

# Load pre-trained model
modelLocation = "AppData\model"
try:
    #model = tf.keras.models.load_model(modelLocation)
    # Temporary Adjustment
    with open(modelLocation,'r') as f:
        print(f.read())
except:
    print("ERROR! Model Not Found! Closing Server")
    exit()   


def identify_animal(image):
    return ["44","elephant",0.95]