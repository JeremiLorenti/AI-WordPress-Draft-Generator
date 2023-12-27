# AI Draft Post Creator

This project is a Python application that utilizes OpenAI's GPT-4 language model to generate draft blog posts based on the latest tech news articles. The application includes a GUI for user interaction and settings configuration.

## Features

- Fetches the latest tech news articles
- Scrapes content from article links
- Uses OpenAI to generate content based on the scraped content
- Creates draft posts with title, AI-generated content, and excerpt on WordPress

## Setup

1. Clone the repository
2. Install the required dependencies using `pip install -r requirements.txt`
3. Run the application using `python newPost.py`

## Configuration

- The OpenAI API key and WordPress settings can be configured through the GUI's "Settings" window.

## File Structure

- `.gitignore` excludes sensitive files and directories
- `newPost.py` contains the main functionality for fetching news articles, generating content, and creating draft posts
- `gui.py` provides the graphical user interface for interacting with the application
- `openAI.py` contains functions for interacting with the OpenAI API
- `utils.py` includes utility functions for sound playback and web scraping
- `wordpress_api.py` handles interactions with the WordPress REST API

## Usage

1. Launch the application to open the main window
2. Enter the number of articles and click "Create New Draft" to generate draft posts
3. Use the "Settings" button to configure OpenAI API key and WordPress settings

Feel free to reach out for any questions or support.
