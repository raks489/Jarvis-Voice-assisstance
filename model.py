# model.py - Handles speech recognition and data processing
import speech_recognition as sr
import requests
import json
import os
from utils.api_manager import get_news, get_weather, search_web

class SpeechModel:
    """Model component handling speech recognition and data processing."""
    
    def __init__(self):
        """Initialize speech recognition engine and data resources."""
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        
        # Adjust for ambient noise when initializing
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
    
    def recognize_speech(self):
        """
        Listen through microphone and convert speech to text.
        Returns recognized text or None if unable to recognize.
        """
        with sr.Microphone() as source:
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                return "Sorry, my speech recognition service is currently unavailable."
    
    def get_news(self, category='general'):
        """Fetch news updates from the news API."""
        return get_news(category)
    
    def get_weather(self, city):
        """Fetch weather information for the specified city."""
        return get_weather(city)
    
    def search_songs(self, query):
        """Search for songs based on the query."""
        # This could connect to a music API or local music library
        # For demonstration, we'll return a simple result
        return f"Found songs matching {query}."
    
    def search_information(self, query):
        """Search the web for information based on the query."""
        return search_web(query)
