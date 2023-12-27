# wordpress_api.py

import requests
import base64
import os

def get_wordpress_categories():
    # Your WordPress website URL
    wordpress_url = os.environ.get('WORDPRESS_URL')
    # REST API endpoint for retrieving categories
    categories_endpoint = wordpress_url + '/wp-json/wp/v2/categories'
    # Send the GET request
    response = requests.get(categories_endpoint)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        return response.json()
    else:
        print(f'Failed to retrieve categories. Status code: {response.status_code}')
        return None

def create_draft_post(post_data):
    # Your WordPress website URL
    wordpress_url = os.environ.get('WORDPRESS_URL')
    # REST API endpoint for creating a draft post
    posts_endpoint = wordpress_url + '/wp-json/wp/v2/posts'
    # Prepare the authentication headers
    username = os.environ.get('WORDPRESS_USERNAME')
    password = os.environ.get('WORDPRESS_APP_PASSWORD')
    token = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': f'Basic {token}'
    }
    # Send the POST request with the post data and headers
    response = requests.post(posts_endpoint, headers=headers, json=post_data)
    # Check if the request was successful
    if response.status_code == 201:
        # Parse the JSON response
        return response.json()
    else:
        print(f'Failed to create draft post. Status code: {response.status_code}')
        return None

# Other WordPress-related functions...

