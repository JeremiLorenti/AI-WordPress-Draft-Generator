import tkinter as tk
from tkinter import simpledialog
import requests
import json
import base64
from openAI import get_openai_response
import threading
import os
import dotenv

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
root.title("AI Draft Post Creator")

# Create a Text widget for the content
text_input = tk.Text(root, height=10, width=50)
text_input.pack()

# Create a Label for loading indication
loading_label = tk.Label(root, text='')
loading_label.pack()

# Create a Button to submit the input
submit_button = tk.Button(root, text="Create Draft Post", command=lambda: on_submit(loading_label))
submit_button.pack()

# Run the GUI loop
root.mainloop()