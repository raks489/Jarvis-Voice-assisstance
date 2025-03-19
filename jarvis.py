# jarvis.py - Main application file
import os
import time
from model import SpeechModel
from view import SpeechView
from controller import CommandController

class Jarvis:
   
    
    def __init__(self):
        
        self.model = SpeechModel()
        self.view = SpeechView()
        self.controller = CommandController(self.model, self.view)
        
    def start(self):
        """Start Jarvis assistant."""
        self.view.speak("Jarvis initialized and ready to assist you.")
        
        while True:
            try:
                # Listen for commands
                self.view.speak_action("Listening...")
                command = self.model.recognize_speech()
                
                if command:
                    # Check for exit command
                    if any(phrase in command.lower() for phrase in ["exit", "stop", "goodbye", "bye"]):
                        self.view.speak("Shutting down. Goodbye!")
                        break
                    
                    # Process command
                    self.view.speak_action(f"Processing: {command}")
                    response = self.controller.process_command(command)
                    
                    # Speak response if not None
                    if response:
                        self.view.speak(response)
                else:
                    self.view.speak("I didn't catch that. Could you repeat?")
                    
            except KeyboardInterrupt:
                self.view.speak("Interrupted. Shutting down.")
                break
            except Exception:
                self.view.speak("Sorry I didn't catch that. Could you repeat?")
                # Small pause to prevent error loops
                time.sleep(1)
        
        self.view.speak("Jarvis has been terminated.")

if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.start()
