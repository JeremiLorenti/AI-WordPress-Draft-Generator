import os
from openai import OpenAI

def get_openai_response(prompt, is_title=False):
    # Assuming you have set your OpenAI API key in your environment variables
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    # System prompt for title generation without HTML formatting
    system_prompt_title = {
        "role": "system",
        "content": "You are a creative assistant. Please provide a single main title for a blog post as plain text. Do NOT include HTML formatting tags like <h1>, <h2>, or <h3> for the title. Keep the title concise and relevant to the content provided. Remember, no HTML formatting tags are required. Do not include HTML document structure tags like <html>, <head>, <body>, or an author's signature."
    }

    # System prompt to provide guidelines to the AI for HTML formatting
    system_prompt_content = {
        "role": "system",
        "content": "You are a creative assistant. Please respond with content formatted in HTML suitable for a blog post body. Use <h3> tags for section headings and <p> tags for paragraphs. Do not include HTML document structure tags like <html>, <head>, <body>, or an author's signature."
    }

    system_prompt = system_prompt_title if is_title else system_prompt_content

    # User prompt with the actual content
    user_prompt = {
        "role": "user",
        "content": prompt,
    }

    # Send the message to the OpenAI API with the system prompt first
    chat_completion = client.chat.completions.create(
        messages=[system_prompt, user_prompt],
        model="gpt-4-1106-preview",
    )

    # Return the content of the response
    return chat_completion.choices[0].message.content
