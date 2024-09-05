from flask import Flask, request, jsonify
from flask_cors import CORS
from image import ImageToTextConverter

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variable to store the latest converted text
latest_converted_text = None

@app.route('/api/convert-image', methods=['POST'])
def convert_image():
    global latest_converted_text

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            # Read the image data from the file
            image_data = file.read()

            # Create an instance of ImageToTextConverter with image data
            converter = ImageToTextConverter(image_data)
            latest_converted_text = converter.extract_text()

            return jsonify({'text': latest_converted_text})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

@app.route('/api/converted-texts', methods=['GET'])
def get_converted_texts():
    # Return the latest converted text or a message if no text is available
    return jsonify({'text': latest_converted_text if latest_converted_text else 'No converted text available.'})

if __name__ == '__main__':
    app.run(debug=True)
