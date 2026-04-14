import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# 1. Categories MUST be in the same order as your folders
categories = ['VeryMildDemented', 'NonDemented', 'ModerateDemented', 'MildDemented']

def get_prediction(img_path):
    # Load the trained model
    # Note: This will only work once your 10/10 epochs are done!
    model = tf.keras.models.load_model('alzheimer_model.h5')
    
    # Resize image to 224x224 to match what the model learned
    img = image.load_img(img_path, target_size=(128, 128))
    
    # Convert image to array and normalize pixels (0 to 1)
    img_array = image.img_to_array(img) / 255.0
    
    # Add batch dimension (Change shape from 224,224,3 to 1,224,224,3)
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    predictions = model.predict(img_array)
    
    # Get the category with the highest score
    predicted_class = categories[np.argmax(predictions[0])]
    confidence = float(np.max(predictions[0]) * 100)
    
    return predicted_class, confidence
    