# Import the os module to interact with the operating system, such as environment variables.
import os
# Import the json module to interact with json files.
import json
# Import the OpenAI class from the openai package to interact with the OpenAI API.
from openai import OpenAI

# Define a function to load settings from settings.json
def load_settings():
    with open('settings.json') as f:
        return json.load(f)

# Define a function named get_openai_response that takes a prompt and an optional is_title flag.
def get_openai_response(prompt, is_title=False):
    # Load settings from settings.json
    settings = load_settings()

    # Create an instance of the OpenAI class using the API key retrieved from the settings.
    client = OpenAI(
        api_key=settings.get("OPENAI_API_KEY"),
    )

    # Define a dictionary for the system prompt when generating a title. This prompt sets the role of the AI.
    system_prompt_title = {
        "role": "system",  # The role is set to 'system' to indicate that this is an instruction.
        # The content provides guidelines for the AI to generate a title without HTML formatting.
        "content": "You are a creative assistant. Please provide a single main title for a blog post as plain text without quotes. Do NOT include HTML formatting tags like <h1>, <h2>, or <h3> for the title. Keep the title concise and relevant to the content provided. Remember, no HTML formatting tags are required. Do not include HTML document structure tags like <html>, <head>, <body>, or an author's signature."
    }

    # Define a dictionary for the system prompt when generating content. This prompt sets the role of the AI.
    system_prompt_content = {
        "role": "system",  # The role is set to 'system' to indicate that this is an instruction.
        # The content provides guidelines for the AI to generate HTML-formatted content for a blog post.
        "content": "You are a creative assistant. Please create a new, original blog post using the following article as source material. Do not plagiarize. Use your creativity to generate a unique article based on the information provided."
    }

    # Choose the appropriate system prompt based on whether the is_title flag is True or False.
    system_prompt = system_prompt_title if is_title else system_prompt_content

    # Define a dictionary for the user prompt that contains the actual content to be processed by the AI.
    user_prompt = {
        "role": "user",  # The role is set to 'user' to indicate that this is the input for the AI.
        "content": prompt,  # The actual content or question that the AI needs to respond to.
    }

    # Send the message to the OpenAI API with the system prompt followed by the user prompt.
    chat_completion = client.chat.completions.create(
        messages=[system_prompt, user_prompt],  # The list of messages to send to the API.
    model="gpt-4-1106-preview",  # The specific model of GPT-4 to use for the completion.
    )

    # Return the content of the response from the AI, which is the generated title or content.
    return chat_completion.choices[0].message.content
