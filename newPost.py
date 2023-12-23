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

def get_wordpress_categories():
    # Your WordPress website URL
    wordpress_url = 'https://thetechnicianstoolchest.com'
    
    # REST API endpoint for retrieving categories
    categories_endpoint = wordpress_url + '/wp-json/wp/v2/categories'
    
    # Send the GET request
    response = requests.get(categories_endpoint)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        categories = response.json()
        return categories
    else:
        print(f'Failed to retrieve categories. Status code: {response.status_code}')
        return None

def select_relevant_categories(post_content):
    # Retrieve all categories
    categories = get_wordpress_categories()
    if not categories:
        print('No categories retrieved from WordPress.')
        return []

    # Prepare a prompt for OpenAI API
    category_names = [cat['name'] for cat in categories]
    prompt = f"Given the blog post content: '{post_content}', which of the following categories is most relevant? " + ", ".join(category_names)

    # Send the prompt to the OpenAI API
    response = get_openai_response(prompt)

    # Debug: Print the response from OpenAI API
    print('Response from OpenAI API:', response)

    # Parse the response to extract the selected categories
    relevant_categories = response.split(', ')
    
    # Debug: Print the relevant categories
    print('Relevant categories:', relevant_categories)

    # Find the IDs of the relevant categories
    relevant_category_ids = [cat['id'] for cat in categories if cat['name'] in relevant_categories]
    relevant_category_ids = [cat['id'] for cat in categories if cat['name'] in relevant_categories]
    
    # Debug: Print the relevant category IDs
    print('Relevant category IDs:', relevant_category_ids)

    return relevant_category_ids

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
        'status': 'draft',  # Set to 'draft' to create a draft post
        'categories': select_relevant_categories(post_content)  # Add relevant categories
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

# Function to create a rounded rectangle on a canvas
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1+radius, y1,
        x1+radius, y1,
        x2-radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1+radius,
        x1, y1
    ]

    return canvas.create_polygon(points, **kwargs, smooth=True)

# Create a Canvas widget for the rounded corners
rounded_canvas = tk.Canvas(main_frame, width=380, height=140, bg='#f0f0f0', highlightthickness=0)
rounded_canvas.pack(pady=(10, 0))

# Draw a rounded rectangle on the Canvas
create_rounded_rectangle(rounded_canvas, 10, 10, 370, 130, radius=20, fill='white')

# Place the Text widget on top of the Canvas
text_input = tk.Text(rounded_canvas, height=5, width=42, padx=10, pady=10, font=('Helvetica', 10), bd=0, highlightthickness=0)
text_input.place(x=20, y=20)

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