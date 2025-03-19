# controller.py - Processes commands and orchestrates actions
import webbrowser
import re
from utils.commands import (
    open_website,
    play_music,
    search_google,
    get_system_info,
    create_reminder,
    tell_time,
    tell_date
)


class CommandController:
    """Controller component handling command processing and business logic."""
    
    def __init__(self, model, view):
        """
        Initialize controller with model and view components.
        
        Args:
            model: The SpeechModel instance
            view: The SpeechView instance
        """
        self.model = model
        self.view = view
        
        # Command patterns
        self.commands = {
            r'open\s+(youtube|google|linkedin|gmail|github)': self.open_website,
            r'search\s+(?:for\s+)?(.*?)(?:\s+on\s+google)?': self.search_web,
            r'play\s+(music|song)(?:\s+by\s+(.+))?': self.play_music,
            r'tell\s+me\s+(?:about\s+)?the\s+news(?:\s+about\s+(.+))?': self.tell_news,
            r'what(?:\'s|\s+is)?\s+(?:the\s+)?weather(?:\s+(?:like|in|at|for)\s+(.+))?':self.get_weather,
            r'weather(?:\s+(?:report|forecast|update))?(?:\s+(?:in|at|for)\s+(.+))?':self.get_weather,
            r'(?:current|today\'s)\s+weather(?:\s+(?:in|at|for)\s+(.+))?':self.get_weather,
            r'tell\s+me\s+(?:about\s+)?(.+)': self.process_command,
            r'(?:what(?:\'s|\s+is)?\s+(?:the\s+)?time(?:\s+(?:now|right now|currently))?|tell\s+(?:me\s+)?(?:the\s+)?time|(?:current|present)\s+time|time\s+(?:now|please|right now))': self.tell_time,
            r'(what\s+(?:is\s+)?today\'?s?\s+date': self.tell_date,
            r'system\s+info(?:rmation)?': self.system_info,
            r'set\s+(?:a\s+)?reminder(?:\s+to\s+(.+))?': self.set_reminder,
            r'help': self.get_help,
        }
    
    def process_command(self, command):
        """
        Process the recognized speech command.
    
         Args:
        command: Text string of user's spoken command
        
        Returns:
        Response string or None if action doesn't require verbal response
        """
        if not command:
            return "I didn't understand that command."
    
         # Convert command to lowercase for better matching
        cmd_lower = command.lower()
    
    # Check each command pattern for a match
        for pattern, handler in self.commands.items():
            match = re.search(pattern, cmd_lower)
            if match:
            # Extract any capture groups and pass to handler
                args = match.groups()
                return handler(*args)
    
    # Fallback - treat unrecognized commands as information queries
    # Remove common filler words
            query = cmd_lower
            fillers = ["please", "can you", "could you", "would you", "i want", "i need"]
            for filler in fillers:
                query = query.replace(filler, "")
    
            query = query.strip()
    
            # If query is too short or just a greeting, give a default response
            if len(query) < 3 or query in ["hi", "hello", "hey"]:
             return f"I'm not sure how to process '{command}'. Try saying 'help' for a list of commands."
    
            # Otherwise, attempt to find information about it
            return self.get_information(query)


        
        # If no matches, return a default response
        return f"I'm not sure how to process '{command}'. Try saying 'help' for a list of commands."
    
    def open_website(self, site):
        """Open a specified website."""
        result = open_website(site)
        return result
    
    def search_web(self, query):
        """Search for information on Google."""
        if not query:
            return "What would you like me to search for?"
        
        result = search_google(query)
        return f"I've searched for {query}"
    
    def play_music(self, music_type, artist=None):
        """Play music, optionally by a specific artist."""
        result = play_music(music_type, artist)
        return result
    
    def tell_news(self, category=None):
        """Get and speak news updates."""
        news_data = self.model.get_news(category)
        
        if not news_data or not news_data.get('articles'):
            return "Sorry, I couldn't fetch any news at the moment."
        
        # Prepare news summary
        articles = news_data['articles'][:3]  # Limit to 3 articles
        
        news_text = "Here are the latest headlines: "
        for i, article in enumerate(articles, 1):
            news_text += f"{i}. {article['title']}. "
        
        return news_text
    
    def get_weather(self, city=None):
        """Get weather information for a city."""
        if not city:
            city = "your current location"  # Default
        
        weather_data = self.model.get_weather(city)
        
        if not weather_data:
            return f"Sorry, I couldn't fetch weather data for {city}."
        
        return f"The weather in {city} is {weather_data['description']} with a temperature of {weather_data['temperature']}°C."
    
    def get_information(self, query):
        """Get general information on a topic."""
        if not query:
            return "What would you like to know about?"
        
        info = self.model.search_information(query)
        
        if not info:
            return f"I couldn't find information about {query}."
        
        return info
    
    def tell_time(self):
        """Tell the current time."""
        return tell_time()
    
    def tell_date(self):
        """Tell today's date."""
        return tell_date()
    
    def system_info(self):
        """Get and speak system information."""
        return get_system_info()
    
    def set_reminder(self, reminder_text=None):
        """Set a reminder with optional text."""
        if not reminder_text:
            return "What would you like me to remind you about?"
        
        result = create_reminder(reminder_text)
        return result
    
    def get_help(self):
        """Provide help information about available commands."""
        help_text = "Here are some commands you can use: "
        help_text += "Open websites like 'open YouTube'. "
        help_text += "Search the web with 'search for cats'. "
        help_text += "Play music with 'play music by Taylor Swift'. "
        help_text += "Get news updates with 'tell me the news'. "
        help_text += "Check the weather with 'what's the weather in New York'. "
        help_text += "Ask about something with 'tell me about Mars'. "
        help_text += "Ask for the time with 'what time is it'. "
        help_text += "Set reminders with 'set reminder to call mom'. "
        help_text += "Get system information with 'system info'. "
        help_text += "Exit by saying 'exit' or 'goodbye'."
        
        return help_text
