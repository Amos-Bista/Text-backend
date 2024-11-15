from googletrans import Translator
from flask import Flask, request, jsonify

class TextTranslator:
    def __init__(self):
        self.translator = Translator()

    def translate(self, text, src_lang='en', dest_lang='ne'):
        """
        Translates text from source language to target language.
        Args:
            text (str): The text to be translated.
            src_lang (str): Source language code (default is 'en' for English).
            dest_lang (str): Destination language code (default is 'ne' for Nepali).
        Returns:
            str: Translated text.
        """
        try:
            translated = self.translator.translate(text, src=src_lang, dest=dest_lang)
            return translated.text
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")

# Flask API





