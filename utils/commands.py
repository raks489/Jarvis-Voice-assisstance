# utils/commands.py - Utility functions for executing commands

import webbrowser
import datetime
import platform
import psutil
import os
import subprocess

def open_website(site):
    """
    Open a specified website.
    
    Args:
        site: Website name (e.g., 'youtube', 'google')
        
    Returns:
        Response message
    """
    site_urls = {
        'youtube': 'https://www.youtube.com',
        'google': 'https://www.google.com',
        'linkedin': 'https://www.linkedin.com',
        'gmail': 'https://mail.google.com',
        'github': 'https://github.com'
    }
    
    site = site.lower()
    if site in site_urls:
        try:
            webbrowser.open(site_urls[site])
            return f"Opening {site.capitalize()}"
        except Exception as e:
            return f"Failed to open {site}. Error: {str(e)}"
    else:
        return f"I don't have {site} in my list of websites."

def search_google(query):
    """
    Search for a query on Google.
    
    Args:
        query: Search query string
        
    Returns:
        Response message
    """
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    try:
        webbrowser.open(search_url)
        return f"Searching Google for {query}"
    except Exception as e:
        return f"Failed to search Google. Error: {str(e)}"

def play_music(music_type, artist=None):
    """
    Play music, optionally by a specific artist.
    
    Args:
        music_type: Type of music ('music' or 'song')
        artist: Optional artist name
        
    Returns:
        Response message
    """
    # For a full implementation, this would connect to a music service API or local music player
    # For demonstration, we'll open YouTube Music with a search
    search_query = "music"
    
    if artist:
        search_query = f"{artist} {music_type}"
    
    music_url = f"https://music.youtube.com/search?q={search_query.replace(' ', '+')}"
    
    try:
        webbrowser.open(music_url)
        if artist:
            return f"Playing {music_type} by {artist}"
        else:
            return f"Playing {music_type}"
    except Exception as e:
        return f"Failed to play music. Error: {str(e)}"

def get_system_info():
    """
    Get system information.
    
    Returns:
        String with system information
    """
    system = platform.system()
    processor = platform.processor()
    memory = psutil.virtual_memory()
    memory_gb = round(memory.total / (1024**3), 2)
    
    # Get CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # Get disk usage
    disk = psutil.disk_usage('/')
    disk_gb = round(disk.total / (1024**3), 2)
    
    info = f"You're running {system} with a {processor} processor. "
    info += f"You have {memory_gb} GB of RAM with {memory.percent}% in use. "
    info += f"Your CPU is at {cpu_percent}% capacity. "
    info += f"Your main disk has {disk_gb} GB total with {disk.percent}% used."
    
    return info

def create_reminder(reminder_text):
    """
    Create a reminder with the given text.
    
    Args:
        reminder_text: Text for the reminder
        
    Returns:
        Response message
    """
    # For a full implementation, this would integrate with a calendar or reminder app
    # For demonstration, we'll just acknowledge the reminder
    
    return f"I've set a reminder: {reminder_text}"

def tell_time():
    """
    Get the current time.
    
    Returns:
        String with current time
    """
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time is {current_time}"

def tell_date():
    """
    Get today's date.
    
    Returns:
        String with today's date
    """
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    return f"Today is {today}"
