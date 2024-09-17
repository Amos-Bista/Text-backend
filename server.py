from flask import Flask, request, jsonify
from flask_cors import CORS
from image import ImageToTextConverter

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global list to store all converted texts
converted_texts = []

@app.route('/api/convert-image', methods=['POST'])
def convert_image():
    """
    API endpoint to receive images, perform OCR, and store the extracted texts.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    # Extract all files from the request
    files = request.files.getlist('file')
    if not files or all(file.filename == '' for file in files):
        return jsonify({'error': 'No selected files'}), 400

    extracted_texts = []
    
    for file in files:
        if file:
            try:
                # Read the image data from the file
                image_data = file.read()

                # Create an instance of ImageToTextConverter with the image data
                converter = ImageToTextConverter(image_data)
                ocr_data = converter.extract_text_with_formatting()

                # Append the extracted text to the list
                extracted_texts.append(ocr_data)  # Updated to append raw OCR data

            except ValueError as e:
                return jsonify({'error': str(e)}), 400

    # Store the extracted texts globally
    converted_texts.extend(extracted_texts)

    return jsonify({'texts': extracted_texts}), 200

@app.route('/api/converted-texts', methods=['GET'])
def get_converted_texts():
    """
    API endpoint to retrieve all converted texts.
    """
    if not converted_texts:
        return jsonify({'message': 'No converted text available.'}), 200

    # Return all converted texts
    return jsonify({'texts': converted_texts}), 200

@app.route('/api/clear-texts', methods=['DELETE'])
def clear_converted_texts():
    """
    API endpoint to clear the stored converted texts.
    """
    global converted_texts
    converted_texts.clear()
    return jsonify({'message': 'All converted texts cleared.'}), 200


if __name__ == '__main__':
    app.run(debug=True)
