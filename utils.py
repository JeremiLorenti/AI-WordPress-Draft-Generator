# utils.py

import winsound

def play_success_sound():
    sound_file_path = 'C://Users//jerem//OneDrive//Desktop//WP//resources//sounds//success-1-6297.wav'
    winsound.PlaySound(sound_file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
