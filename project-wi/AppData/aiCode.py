# Project WI - AppData.aiCode
# v1.0
# Contains the Identifier AI

#Import Libraries
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from keras.preprocessing import image # type: ignore
from keras.applications import imagenet_utils # type: ignore

# Load model
model = tf.keras.applications.mobilenet_v2.MobileNetV2()

def identify_animal(image):
    resized_image=image.resize((224,224))
    #Preprocess
    resized_image = np.array(resized_image)
    final_image = np.expand_dims(resized_image, axis=0)
    final_image = tf.keras.applications.mobilenet.preprocess_input(final_image)
    # Predict
    predictions = model.predict(final_image)
    # Decode and Classify
    results = imagenet_utils.decode_predictions(predictions,top=3)
    print(results)
    print(fiveTypeClassifier(results[0][0][1]))
    return [results[0][0][1],fiveTypeClassifier(results[0][0][1]),results[0][0][2]]

def fiveTypeClassifier(animal):
    animal= animal.casefold()
    detectableAnimals = ['elephant','tiger','crocodile','boar','human poachers']
    keywords = ['elephant','tiger','crocodile','boar','man']
    if "elephant" in animal:
        return detectableAnimals[0]
    elif "tiger" in animal:
        return detectableAnimals[1]
    elif "crocodile" in animal:
        return detectableAnimals[2]
    elif "boar" in animal:
        return detectableAnimals[3]
    elif "man" in animal:
        return detectableAnimals[4]
    else:
        return "unidentified"
