from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Lambda, GlobalAveragePooling2D, Dense, Input
from tensorflow.keras.applications.xception import Xception, preprocess_input

app = Flask(__name__)

# Define the custom function used in your Lambda layer
def xception_preprocessing(img):
    return preprocess_input(img)

# Function to build the model architecture
def build_model():
    base_model = Xception(include_top=False, input_tensor=Input(shape=(320, 320, 3)), weights=None)
    base_model.trainable = False  # Make the base model non-trainable

    model = Sequential([
        Input(shape=(320, 320, 3)),  # Explicitly define an Input layer
        Lambda(preprocess_input, name='preprocessing'),
        base_model,
        GlobalAveragePooling2D(),
        Dense(12, activation='softmax')  # Assuming there are 12 classes
    ])
    return model

class_info = {
    0: {"name": "Paper", "recycling_instructions": "Drop off at any recycling bin designated for paper. Ensure it is dry and free from food residue."},
    1: {"name": "Cardboard", "recycling_instructions": "Flatten boxes and remove any non-paper packing materials."},
    2: {"name": "Plastic", "recycling_instructions": "Rinse and sort plastics by number. Check local facilities for specific types accepted."},
    3: {"name": "Metal", "recycling_instructions": "Clean and sort by type. Most metals like aluminum and steel can be recycled curbside."},
    4: {"name": "Trash", "recycling_instructions": "Not recyclable. Dispose of as general waste."},
    5: {"name": "Battery", "recycling_instructions": "Batteries should be recycled at designated drop-off locations due to hazardous materials."},
    6: {"name": "Shoes", "recycling_instructions": "Donate if in good condition or recycle at textile recycling points."},
    7: {"name": "Clothes", "recycling_instructions": "Donate wearable clothes or recycle at textile recycling points."},
    8: {"name": "Green Glass", "recycling_instructions": "Rinse and recycle at glass recycling points."},
    9: {"name": "Brown Glass", "recycling_instructions": "Rinse and recycle at glass recycling points."},
    10: {"name": "White Glass", "recycling_instructions": "Rinse and recycle at glass recycling points."},
    11: {"name": "Biological", "recycling_instructions": "Compost if possible, or dispose of in biodegradable waste bins."}
}

# Load the model
model = build_model()
model.load_weights('eco-track.h5')  # Ensure this is the path to your weights file

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the EcoTrack Recycling Assistant!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        image = Image.open(file.stream).convert('RGB')
        app.logger.info('Image opened and converted to RGB')
        
        image = image.resize((320, 320))
        app.logger.info('Image resized to 320x320')
        
        image = np.array(image)
        app.logger.info('Image converted to numpy array')
        
        image = np.expand_dims(image, axis=0)
        app.logger.info('Image expanded with new axis')
        
        prediction = model.predict(image)
        app.logger.info('Prediction made')
        
        predicted_class = np.argmax(prediction, axis=1)[0]
##        predicted_class = int(predicted_class)
        app.logger.info(f'Predicted class: {predicted_class}')
        
        class_data = class_info.get(predicted_class, {"name": "Unknown", "recycling_instructions": "No instructions available."})
        app.logger.info(f'Class data retrieved: {class_data}')
        
        return jsonify({
            'predicted_class': int(predicted_class), 
            'class_name': class_data['name'], 
            'recycling_instructions': class_data['recycling_instructions']
        })
    except Exception as e:
        app.logger.error(f'Error processing image: {type(e).__name__}, {str(e)}')
        return jsonify({'error': f'Error processing image: {type(e).__name__}', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
