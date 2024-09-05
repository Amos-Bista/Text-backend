import cv2
import pytesseract
import numpy as np
from io import BytesIO

# If you're on Windows, specify the path to Tesseract executable:
# Comment this out if you're using Linux or macOS
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ImageToTextConverter:
    def __init__(self, image_data):
        self.image_data = image_data

    def load_image(self):
        """
        Load the image from bytes.
        
        Returns:
        - numpy.ndarray: Loaded image
        """
        image = cv2.imdecode(np.frombuffer(self.image_data, np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Image could not be loaded.")
        return image

    def convert_to_grayscale(self, image):
        """
        Convert the image to grayscale.
        
        Parameters:
        - image: numpy.ndarray, the image to convert
        
        Returns:
        - numpy.ndarray: Grayscale image
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def perform_ocr(self, gray_image):
        """
        Perform OCR on the grayscale image.
        
        Parameters:
        - gray_image: numpy.ndarray, the grayscale image
        
        Returns:
        - str: Extracted text from the image
        """
        return pytesseract.image_to_string(gray_image)

    def extract_text(self):
        """
        Extract text from the image using OCR.
        
        Returns:
        - str: Extracted text from the image
        """
        image = self.load_image()
        gray_image = self.convert_to_grayscale(image)
        text = self.perform_ocr(gray_image)
        return text
