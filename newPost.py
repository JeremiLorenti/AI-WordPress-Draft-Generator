import tkinter as tk
from tkinter import ttk  # Import ttk for standard tkinter widgets
import customtkinter as ctk  # Import customtkinter for custom widgets
from openAI import get_openai_response
import threading
from wordpress_api import get_wordpress_categories, create_draft_post
from utils import play_success_sound, scrape_content_from_url  # Import the new function to scrape content
from news_fetcher import fetch_latest_tech_news
import asyncio

async def select_relevant_categories(post_content):
    # Retrieve all categories
    categories = await get_wordpress_categories()
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

async def on_submit(loading_label, num_articles, num_posts, progress_label):
    # Fetch the latest news articles
    latest_articles = fetch_latest_tech_news(num_articles=int(num_articles))

    post_urls = []  # List to collect the URLs of the new draft posts
    for article in latest_articles[:int(num_posts)]:
        try:
            # Scrape the content from the article link
            article_content = scrape_content_from_url(article.link)

            # Use the AI to generate content based on the scraped content
            ai_prompt = (
                f"Given the following content: '{article_content}'\n"
                "Please rewrite it in HTML format suitable for a blog post. Start the article with an opening paragraph. You do not need to include a beginning title or heading"
                "since the main title is handled separately. Use HTML tags for styling such as "
                "<p> for paragraphs, <strong> for bold text, <em> for italics, "
                "and <ul> or <ol> with <li> for lists. Do not include backticks (`), markdown formatting such as hashtags for headers or "
                "asterisks for lists, or HTML document structure tags like <!DOCTYPE>, <html>, <head>, or <body>. Also do not include `html at the start or ` at the end. The output should be a properly formated article containing only the article content itself, free of formatting tags or encodings.\n"
            )
           
            ai_generated_content = get_openai_response(ai_prompt)

            # Construct post_data with title, AI-generated content, and excerpt
            post_data = {
                'title': article.title,
                'content': ai_generated_content,
                'excerpt': article.summary
            }

            # Collect the URL of the new draft post
            post_url = await create_draft_post(post_data)
            post_urls.append(post_url)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            raise e

    # Play success sound
    play_success_sound()

    # Update the loading label
    loading_label.configure(text="Drafts Successfully Created!")
    
    # Return the list of URLs of the new draft posts
    return post_urls
