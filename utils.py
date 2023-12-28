import json
from urllib.parse import urlparse
import winsound
import requests
from bs4 import BeautifulSoup

settings_file_path = 'settings.json'

def play_success_sound():
    sound_file_path = 'C://Users//jerem//OneDrive//Desktop//WP//resources//sounds//success-1-6297.wav'
    winsound.PlaySound(sound_file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)

def scrape_content_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()

def is_valid_api_key(api_key):
    # Check if the API key is a non-empty string
    return bool(api_key and api_key.strip())

def is_valid_url(url):
    # Check if the URL is well-formed by using urlparse
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])

def save_settings(openai_api_key, wordpress_url, wordpress_username, wordpress_password, article_preview):
    # Validate the OpenAI API key
    if not is_valid_api_key(openai_api_key):
        raise ValueError("The OpenAI API key is invalid.")

    # Validate the WordPress URL
    if not is_valid_url(wordpress_url):
        raise ValueError("The WordPress URL is invalid.")

    # Save the settings to a JSON file
    settings = {
        'OPENAI_API_KEY': openai_api_key,
        'WORDPRESS_URL': wordpress_url,
        'WORDPRESS_USERNAME': wordpress_username,
        'WORDPRESS_PASSWORD': wordpress_password,
        'ARTICLE_PREVIEW': article_preview
    }
    with open(settings_file_path, 'w') as settings_file:
        json.dump(settings, settings_file, indent=4)

def load_settings():
    # Load the settings from a JSON file
    try:
        with open(settings_file_path, 'r') as settings_file:
            settings = json.load(settings_file)
            return settings
    except FileNotFoundError:
        # If the settings file does not exist, return None
        return None
