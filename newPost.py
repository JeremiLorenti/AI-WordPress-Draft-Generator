import tkinter as tk
from tkinter import ttk  # Import ttk module for themed widgets
from tkinter import simpledialog
import requests
import json
import base64
from openAI import get_openai_response
import threading
import os
import dotenv
import winsound

def play_success_sound():
    sound_file_path = 'C://Users//jerem//OneDrive//Desktop//WP//resources//sounds//success-1-6297.wav'
    winsound.PlaySound(sound_file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)

def create_draft_post(content, loading_label):
    # Update the loading label
    loading_label.config(text='Generating title... Please wait.')
    loading_label.update_idletasks()

    # Generate a title using OpenAI based on a description of the content
    title_prompt = "Create a catchy title for a blog post based on this content summary: " + content[:60]  # Use the first 60 characters as a summary
    post_title = get_openai_response(title_prompt, is_title=True).strip()  # Pass is_title=True for title generation

    # Ensure the title is no longer than 20 words
    post_title_words = post_title.split()
    if len(post_title_words) > 20:
        post_title = ' '.join(post_title_words[:20])

    # Update the loading label
    loading_label.config(text='Generating content... Please wait.')
    loading_label.update_idletasks()

    # Get the content from OpenAI
    content_prompt = "Write a blog post based on this content summary: " + content
    post_content = get_openai_response(content_prompt, is_title=False).strip()  # Pass is_title=False for content generation

    # Your WordPress website URL
    wordpress_url = 'https://thetechnicianstoolchest.com'

    # REST API endpoint for creating a new post
    endpoint = wordpress_url + '/wp-json/wp/v2/posts'

    # The data for the new post, with 'status' set to 'draft'
    post_data = {
        'title': post_title,
        'content': post_content,
        'status': 'draft'  # Set to 'draft' to create a draft post
    }

    # Your username and application password from .env
    username=os.environ.get('WORDPRESS_USERNAME')
    app_password=os.environ.get('WORDPRESS_APP_PASSWORD')


    # Encoding the username and application password
    token = base64.b64encode(f"{username}:{app_password}".encode())
    headers = {
        'Authorization': f'Basic {token.decode()}',
        'Content-Type': 'application/json'
    }

# Send the POST request
    response = requests.post(endpoint, headers=headers, data=json.dumps(post_data))

    # Check the response and update the loading label with error logging
    if response.status_code == 201:
        loading_label.config(text='Draft post created successfully!')
        # Play the success sound clip
        play_success_sound()
    else:
        # Log the status code and response content for debugging
        print(f'Failed to create draft post. Status code: {response.status_code}')
        print(f'Response content: {response.content.decode()}')
        loading_label.config(text='Failed to create draft post. Please check the logs.')

    loading_label.update_idletasks()

def on_submit(loading_label):
    content = text_input.get("1.0", tk.END)
    threading.Thread(target=create_draft_post, args=(content, loading_label)).start()
    text_input.delete("1.0", tk.END)

# Create the main window
root = tk.Tk()
root.title("AI Draft Post Creator")  # Set a window title
root.configure(background='#f0f0f0')  # Set the background color of the window

# Set the window size and position
root.geometry('600x450+50+50')  # Width x Height + X position + Y position

# Create a style object and configure styles
style = ttk.Style()
style.configure('TButton', padding=6, font=('Helvetica', 10))
style.configure('TLabel', padding=6, background='#f0f0f0', font=('Helvetica', 10))
style.configure('TEntry', padding=6)
style.configure('TFrame', background='#f0f0f0')

# Create a frame for padding and layout management
main_frame = ttk.Frame(root, padding="20 20 20 20", style='TFrame')
main_frame.pack(fill=tk.BOTH, expand=True)

# Create a Label for the title
title_label = ttk.Label(main_frame, text="AI Draft Post Creator", style='TLabel', font=('Helvetica', 16, 'bold'))
title_label.pack()

# Create a Separator
separator = ttk.Separator(main_frame, orient='horizontal')
separator.pack(fill='x', pady=10)

# Create a Label for instructions
instructions_label = ttk.Label(main_frame, text="Enter the content for the blog post below:", style='TLabel')
instructions_label.pack()

# Create a Text widget for the content with padding
text_input = tk.Text(main_frame, height=10, width=50, padx=10, pady=10, font=('Helvetica', 10))
text_input.pack()

# Create another Separator
separator2 = ttk.Separator(main_frame, orient='horizontal')
separator2.pack(fill='x', pady=10)

# Create a Label for loading indication
loading_label = ttk.Label(main_frame, text='', style='TLabel')
loading_label.pack()

# Create a Button to submit the input with padding
submit_button = ttk.Button(main_frame, text="Create Draft Post", command=lambda: on_submit(loading_label), style='TButton')
submit_button.pack(pady=10)

# Ensure the window opens in the center of the screen
root.eval('tk::PlaceWindow . center')

# Run the GUI loop
root.mainloop()