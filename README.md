# AI Draft Post Creator

This application uses OpenAI's GPT model to generate draft blog posts. It takes a content summary as input and generates a catchy title and content for a blog post.

## Files

- `newPost.py`: This is the main script that runs the application. It uses tkinter for the GUI and makes a POST request to a WordPress website to create a draft post.

- `openAI.py`: This script contains the function `get_openai_response` which communicates with the OpenAI API to generate the title and content of the blog post.

## Usage

1. Run `newPost.py`.
2. Enter a summary of the content you want in the blog post.
3. Click "Create Draft Post".

The application will then generate a title and content for the blog post and create a draft post on the WordPress website.

## Environment Variables

The application requires the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key.
- `WORDPRESS_USERNAME`: Your WordPress username.
- `WORDPRESS_APP_PASSWORD`: Your WordPress application password.

These should be set in a `.env` file in the same directory as the scripts.
