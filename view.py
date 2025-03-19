# view.py - Manages text-to-speech and user interface feedback
import os
import tempfile
from gtts import gTTS
import playsound
import pyttsx3

class SpeechView:
    """View component handling speech output and user feedback."""
    
    def __init__(self):
        """Initialize text-to-speech engines."""
        # Primary TTS engine (Google)
        self.use_google_tts = True
        
        # Backup TTS engine (pyttsx3)
        self.backup_engine = pyttsx3.init()
        self.backup_engine.setProperty('rate', 220)
        self.backup_engine.setProperty('volume', 1.0)
        
        # Set voice properties for backup engine
        voices = self.backup_engine.getProperty('voices')
        # Try to set a male voice for more Jarvis-like experience
        for voice in voices:
            if "male" in voice.name.lower():
                self.backup_engine.setProperty('voice', voice.id)
                break
        
        # Create temp directory for audio files if it doesn't exist
        self.temp_dir = os.path.join(tempfile.gettempdir(), "jarvis_audio")
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        
        # Counter for unique filenames
        self.file_counter = 0
    
    def speak(self, text):
        """Convert text to speech and play it."""
        if not text:
            return
        
        print(f"Jarvis: {text}")
        
        if self.use_google_tts:
            try:
                # Create a unique filename
                self.file_counter += 1
                temp_file = os.path.join(self.temp_dir, f"jarvis_speech_{self.file_counter}.mp3")
                
                # Generate speech using Google TTS
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(temp_file)
                
                # Play the generated speech
                playsound.playsound(temp_file, True)
                
                # Clean up the temporary file
                try:
                    os.remove(temp_file)
                except:
                    # If removal fails, it's not critical
                    pass
                    
            except Exception as e:
                print(f"Google TTS error: {e}")
                # Fall back to pyttsx3
                self.backup_engine.say(text)
                self.backup_engine.runAndWait()
        else:
            # Use pyttsx3 directly
            self.backup_engine.say(text)
            self.backup_engine.runAndWait()
    
    def speak_action(self, text):
        """Print action text without speaking it."""
        print(f"[Action] {text}")
