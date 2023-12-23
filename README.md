# AI Draft Post Creator

This is a Python application that uses OpenAI to generate draft blog posts.

## Files

### newPost.py

This script creates a GUI for the user to input the content for a blog post. It then uses OpenAI to generate a title and content for the post, and creates a draft post on a WordPress website.

### openAI.py

This script contains the function `get_openai_response`, which sends a prompt to the OpenAI API and returns the generated response.

## Usage

1. Run `newPost.py`.
2. Enter the content for the blog post in the text box.
3. Click "Create Draft Post" to generate the post and create a draft on the WordPress website.

## Requirements

- Python 3
- tkinter
- requests
- json
- base64
- threading
- os
- dotenv
- winsound
- OpenAI API key
- WordPress website with REST API enabled
- WordPress username and application password
