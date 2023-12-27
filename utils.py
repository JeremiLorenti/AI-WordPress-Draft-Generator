# utils.py

import winsound
import requests
from bs4 import BeautifulSoup

def play_success_sound():
    sound_file_path = 'C://Users//jerem//OneDrive//Desktop//WP//resources//sounds//success-1-6297.wav'
    winsound.PlaySound(sound_file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
def scrape_content_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()
