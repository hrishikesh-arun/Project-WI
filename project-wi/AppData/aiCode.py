#Import Libraries
import tensorflow as tf
import numpy as np
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
    results = imagenet_utils.decode_predictions(predictions,top=5)
    print(results)
    print(typeClassifier(results[0][0][1]))
    return [results[0][0][1],typeClassifier(results[0][0][1]),results[0][0][2]]

def typeClassifier(animal):
    animal= animal.casefold()
    detectableAnimals = ['elephant','tiger','crocodile','boar','bear','lion','human']
    keywords = ['eleph','tiger','croc','boar','bear','lion','man'] # Words to search
    detectables = list(zip(detectableAnimals,keywords))
    for i in range(len(detectables)):
        if detectables[i][1] in animal:
            return detectables[i][0]
    return "unidentified"
