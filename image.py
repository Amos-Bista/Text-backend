import cv2
import pytesseract
import numpy as np
from pytesseract import Output

class ImageToTextConverter:
    def __init__(self, image_data, visualize=False):
        self.image_data = image_data
        self.visualize = visualize  # Optional parameter to visualize results

    def load_image(self):
        # Load image from byte data
        image = cv2.imdecode(np.frombuffer(self.image_data, np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Image could not be loaded.")
        return image

    def convert_to_grayscale(self, image):
        # Convert to grayscale for better OCR performance
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def perform_ocr_with_details(self, gray_image):
        # Get detailed OCR information including bounding boxes and text
        ocr_data = pytesseract.image_to_data(gray_image, output_type=Output.DICT)
        return ocr_data

    def extract_text_with_formatting(self):
        """Main method to extract text and provide formatting info."""
        # Load and preprocess image
        image = self.load_image()
        gray_image = self.convert_to_grayscale(image)
        ocr_data = self.perform_ocr_with_details(gray_image)

        # Organize text by lines and paragraphs
        lines = {}
        for i in range(len(ocr_data['text'])):
            if int(ocr_data['conf'][i]) > 60:  # Filter by confidence level
                line_num = ocr_data['line_num'][i]
                if line_num not in lines:
                    lines[line_num] = []
                lines[line_num].append((ocr_data['left'][i], ocr_data['text'][i]))

        # Sort lines by their vertical position (top) and then reconstruct text
        sorted_lines = sorted(lines.items(), key=lambda x: min([y[0] for y in x[1]]))
        formatted_text = "\n".join(
            " ".join(word for _, word in sorted(line[1]))
            for line in sorted_lines
        )

        # Optionally visualize bounding boxes and OCR results
        if self.visualize:
            self.visualize_ocr(image, ocr_data)

        return formatted_text  # Return the formatted text with original spacing and alignment

    def visualize_ocr(self, image, ocr_data):
        """Draw bounding boxes around detected text for visualization."""
        for i in range(len(ocr_data['text'])):
            if int(ocr_data['conf'][i]) > 60:  # Filter by confidence level
                (x, y, w, h) = (ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i])
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(image, ocr_data['text'][i], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        cv2.imshow('OCR Visualization', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Usage Example:
# converter = ImageToTextConverter(image_data, visualize=True)
# formatted_text = converter.extract_text_with_formatting()
# print(formatted_text)
