# Create a Button to save the OpenAI API key and WordPress credentials
import tkinter as tk
from tkinter import ttk  # Import ttk for standard tkinter widgets
import customtkinter as ctk  # Import customtkinter for custom widgets
from openAI import get_openai_response
import threading
from wordpress_api import get_wordpress_categories, create_draft_post
from utils import play_success_sound, scrape_content_from_url  # Import the new function to scrape content
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
        # Scrape the content from the article link
        article_content = scrape_content_from_url(article.link)

        # Use the AI to generate content based on the scraped content
        ai_generated_content = get_openai_response(article_content)

        # Construct post_data with title, AI-generated content, and excerpt
        post_data = {
            'title': article.title,
            'content': ai_generated_content,
            'excerpt': article.summary
        }
        thread = threading.Thread(target=create_draft_post, args=(post_data,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

# Create the main window
def create_main_window():
    from gui import create_main_window
    root, num_articles, spinner_label = create_main_window()

    # Run the GUI loop
    root.mainloop()
if __name__ == "__main__":
    create_main_window()
