# Create a Button to save the OpenAI API key and WordPress credentials
import tkinter as tk
from tkinter import ttk  # Import ttk for standard tkinter widgets
import customtkinter as ctk  # Import customtkinter for custom widgets
from openAI import get_openai_response
import threading
from wordpress_api import get_wordpress_categories, create_draft_post
from utils import play_success_sound
from gui import create_main_window
from news_fetcher import fetch_latest_tech_news

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
    
    # Debug: Print the relevant category IDs
    print('Relevant category IDs:', relevant_category_ids)

    return relevant_category_ids

def on_submit(loading_label, num_articles, num_posts):
    # Fetch the latest news articles
    latest_articles = fetch_latest_tech_news(num_articles=int(num_articles))

    threads = []
    for article in latest_articles[:int(num_posts)]:
        thread = threading.Thread(target=create_draft_post, args=(loading_label, article.link))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

# Create the main window
root = create_main_window()

# Run the GUI loop
root.mainloop()
