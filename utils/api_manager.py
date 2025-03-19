# utils/api_manager.py - Functions for API interactions

import requests
import json
import os
from datetime import datetime
import webbrowser
# Add your API keys here or load from environment variables
# NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "your_news_api_key")
# WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "your_weather_api_key")

# For demonstration purposes, using placeholder keys
NEWS_API_KEY = "Your API"
WEATHER_API_KEY = "Your API"

def get_news(category='general'):
    """
    Fetch news from News API.
    
    Args:
        category: News category (general, business, technology, etc.)
        
    Returns:
        Dictionary with news data or None if request failed
    """
    base_url = "https://newsapi.org/v2/top-headlines"
    
    params = {
        'country': 'us',
        'category': category,
        'apiKey': NEWS_API_KEY
    }
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"News API request failed with status {response.status_code}: {response.text}")
            # Return mock data for demonstration
            return {
                'articles': [
                    {'title': 'This is a sample news headline for demonstration purposes.'},
                    {'title': 'Another sample headline since the actual API request failed.'},
                    {'title': 'A third sample news item. In production, use a valid API key.'}
                ]
            }
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return None

def get_weather(city):
    """
    Fetch weather data from OpenWeatherMap API.
    
    Args:
        city: City name
        
    Returns:
        Dictionary with weather data or None if request failed
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric'  # For Celsius
    }
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return {
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
        else:
            print(f"Weather API request failed with status {response.status_code}: {response.text}")
            # Return mock data for demonstration
            return {
                'temperature': 22,
                'description': 'partly cloudy',
                'humidity': 65,
                'wind_speed': 5.5
            }
    except Exception as e:
        print(f"Error fetching weather: {str(e)}")
        return None

def search_web(query):
    """
    Search the web for information on a query using Google Search API.
    
    Args:
        query: Search query
        
    Returns:
        String with search information
    """
    # You need to register for a Google API key and Custom Search Engine ID
    API_KEY = "YOUR_GOOGLE_API_KEY"  # Replace with your Google API key
    SEARCH_ENGINE_ID = "YOUR_SEARCH_ENGINE_ID"  # Replace with your Search Engine ID
    
    base_url = "https://www.googleapis.com/customsearch/v1"
    
    params = {
        'q': query,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'num': 3  # Number of results to return
    }
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            search_results = response.json()
            
            if 'items' in search_results and len(search_results['items']) > 0:
                # Format the top 3 results
                result_text = f"Here's what I found about {query}:\n\n"
                
                for i, item in enumerate(search_results['items'][:3], 1):
                    title = item.get('title', 'No title')
                    snippet = item.get('snippet', 'No description available')
                    
                    result_text += f"{i}. {title}\n"
                    result_text += f"   {snippet}\n\n"
                
                return result_text
            else:
                return f"I couldn't find any information about {query}."
                
        else:
            # Fallback to browser search if API fails
            return search_google_browser(query)
            
    except Exception as e:
        print(f"Error searching the web: {str(e)}")
        # Fallback to browser search
        return search_google_browser(query)

def search_google_browser(query):
    """
    Fallback function that searches Google by opening the browser.
    Doesn't require an API key.
    """
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    try:
        webbrowser.open(search_url)
        return f"I've searched for '{query}' and opened the results in your browser."
    except Exception as e:
        return f"Failed to search Google. Error: {str(e)}"