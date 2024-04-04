
import base64
from io import BytesIO
import numpy as np
from torchvision import transforms
from PIL import Image
import tensorflow as tf
from tensorflow import convert_to_tensor
from tensorflow.keras.models import load_model
from scipy.ndimage import zoom


CLASS_NAMES = ['Healthy', 'Powdery', 'Rust']
def predict(data,request):
    path= '../../model/1'
    model = load_model(path)
    if model:
        print("Model loaded successfully.")
        data = zoom(data, (1, 256 / data.shape[1], 256 / data.shape[2], 1))
        predictions = model.predict(data)
        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        confidence = round(100 * np.max(predictions[0]), 2)

        # Convert the image to base64
        image_pil = Image.fromarray(data[0].astype('uint8'))
        buffered = BytesIO()
        image_pil.save(buffered, format="JPEG")
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Store the values in the session
        request.session['predicted_class'] = predicted_class
        request.session['confidence'] = confidence
        request.session['base64_image'] = base64_image

        
        return (predicted_class,confidence)
    else:
        print("Failed to load the model.")
