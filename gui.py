import tkinter as tk
from tkinter import ttk  # Import ttk for standard tkinter widgets
import customtkinter as ctk  # Import customtkinter for custom widgets
import os
import json
import tkinter.messagebox as msgbox
import re
from urllib.parse import urlparse

# Define the path to the settings file
settings_file_path = 'settings.json'

def is_valid_api_key(api_key):
    # Check if the API key is a non-empty string
    return bool(api_key and api_key.strip())

def is_valid_url(url):
    # Check if the URL is well-formed by using urlparse
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])

def save_settings(openai_api_key, wordpress_url, wordpress_username, wordpress_password):
    # Validate the OpenAI API key
    if not is_valid_api_key(openai_api_key):
        msgbox.showerror("Error", "The OpenAI API key is invalid.")
        return

    # Validate the WordPress URL
    if not is_valid_url(wordpress_url):
        msgbox.showerror("Error", "The WordPress URL is invalid.")
        return

    try:
        # Save the settings to a JSON file
        settings = {
            'OPENAI_API_KEY': openai_api_key,
            'WORDPRESS_URL': wordpress_url,
            'WORDPRESS_USERNAME': wordpress_username,
            'WORDPRESS_PASSWORD': wordpress_password
        }
        with open(settings_file_path, 'w') as settings_file:
            json.dump(settings, settings_file, indent=4)
        # Show a confirmation message
        msgbox.showinfo("Settings Saved", "Your settings have been saved successfully.")
    except Exception as e:
        # Show an error message
        msgbox.showerror("Error", f"An error occurred while saving settings: {e}")

def load_settings():
    # Load the settings from a JSON file
    try:
        with open(settings_file_path, 'r') as settings_file:
            settings = json.load(settings_file)
            return settings
    except FileNotFoundError:
        # If the settings file does not exist, return None
        return None

    # Create a button to open settings window
def create_settings_window():
    settings_root = tk.Toplevel()
    settings_root.title("Settings")
    
    # Set a fixed width and height for the settings window
    settings_root.geometry('400x350')  # Width x Height
    
    # Center the settings window on the screen
    window_width = 400
    window_height = 450
    screen_width = settings_root.winfo_screenwidth()
    screen_height = settings_root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    settings_root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # Create a label frame for API settings
    api_settings_frame = ctk.CTkFrame(settings_root)
    api_settings_frame.pack(pady=10, padx=10, fill='both', expand=True)

    openai_api_label = ctk.CTkLabel(api_settings_frame, text="OpenAI API Key:", font=("Lato", 10))
    openai_api_label.pack(pady=(10, 0))
    openai_api_entry = ctk.CTkEntry(api_settings_frame, width=300, placeholder_text="Enter your OpenAI API key", font=("Lato", 10))
    openai_api_entry.pack(pady=(0, 10))

    # Create a label frame for WordPress settings
    wordpress_settings_frame = ctk.CTkFrame(settings_root)
    wordpress_settings_frame.pack(pady=10, padx=10, fill='both', expand=True)

    wordpress_url_label = ctk.CTkLabel(wordpress_settings_frame, text="WordPress URL:", font=("Lato", 10))
    wordpress_url_label.pack(pady=(10, 0))
    wordpress_url_entry = ctk.CTkEntry(wordpress_settings_frame, width=300, placeholder_text="Enter your WordPress URL", font=("Lato", 10))
    wordpress_url_entry.pack(pady=(0, 10))

    wordpress_username_label = ctk.CTkLabel(wordpress_settings_frame, text="WordPress Username:", font=("Lato", 10))
    wordpress_username_label.pack(pady=(10, 0))
    wordpress_username_entry = ctk.CTkEntry(wordpress_settings_frame, width=300, placeholder_text="Enter your WordPress username", font=("Lato", 10))
    wordpress_username_entry.pack(pady=(0, 10))

    wordpress_password_label = ctk.CTkLabel(wordpress_settings_frame, text="WordPress Password:", font=("Lato", 10))
    wordpress_password_label.pack(pady=(10, 0))
    wordpress_password_entry = ctk.CTkEntry(wordpress_settings_frame, width=300, show="*", placeholder_text="Enter your WordPress password", font=("Lato", 10))
    wordpress_password_entry.pack(pady=(0, 10))

    # Load existing settings and populate the fields
    existing_settings = load_settings()
    if existing_settings:
        openai_api_entry.insert(0, existing_settings.get('OPENAI_API_KEY', ''))
        wordpress_url_entry.insert(0, existing_settings.get('WORDPRESS_URL', ''))
        wordpress_username_entry.insert(0, existing_settings.get('WORDPRESS_USERNAME', ''))
        wordpress_password_entry.insert(0, existing_settings.get('WORDPRESS_PASSWORD', ''))

    # Customize the Save Button
    save_button = ctk.CTkButton(settings_root, text="Save Settings", command=lambda: save_settings(
        openai_api_entry.get(),
        wordpress_url_entry.get(),
        wordpress_username_entry.get(),
        wordpress_password_entry.get()
    ), corner_radius=10, fg_color="#00A2FF", hover_color="#007ACC", font=("Lato", 10))
    save_button.pack(pady=10)

    return settings_root

def create_main_window():
    root = tk.Tk()
    root.title("AI Draft Post Creator")  # Set a window title
    # Set window background color to dark gray
    root.configure(bg="dark gray")
    root.tk_setPalette(background='dark gray')

    # Set the appearance mode to "Dark"
    ctk.set_appearance_mode("Dark")

    # Set a modern color scheme
    ctk.set_default_color_theme("dark-blue")  # You can choose from predefined themes or create your own

    # Set the window size and position
    root.geometry('350x250+50+50')  # Width x Height + X position + Y position

    # Ensure the window opens in the center of the screen
    root.eval('tk::PlaceWindow . center')

    # Create a label and add it to the window using pack layout manager
    
    label = ctk.CTkLabel(root, text="Welcome to AI Draft Post Creator", font=('Lato', 20, 'bold'))
    label.pack(pady=10)

    # Create a button to open settings window
    settings_button = ctk.CTkButton(root, text="Settings", command=create_settings_window, font=("Lato", 10))
    settings_button.pack(pady=10)

    # Create a button and add it to the window using pack layout manager
    create_button = ctk.CTkButton(root, text="Create New Draft", font=("Lato", 10))
    create_button.pack(pady=10)

    return root
