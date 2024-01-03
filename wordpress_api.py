import httpx
import base64
import os
import json



# Get WordPress credentials from settings.json
def get_wordpress_credentials():
    with open('settings.json') as f:
        settings = json.load(f)
    return settings['wordpress']['username'], settings['wordpress']['password']

# Get WordPress URL from settings.json
def get_wordpress_url():
    with open('settings.json') as f:
        settings = json.load(f)
    return settings['WORDPRESS_URL']

async def get_draft_posts():
    wordpress_url = get_wordpress_url()
    # Ensure there's no trailing slash on the URL to avoid double slashes in the endpoint
    if wordpress_url.endswith('/'):
        wordpress_url = wordpress_url.rstrip('/')
    posts_endpoint = wordpress_url + '/wp-json/wp/v2/posts?status=draft'
    
    # Get WordPress credentials and encode them for Basic Auth
    wordpress_username, wordpress_password = get_wordpress_credentials()
    token = base64.b64encode(f"{wordpress_username}:{wordpress_password}".encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': f'Basic {token}'
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(posts_endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        error_message = f'Failed to retrieve draft posts. Status code: {response.status_code}'
        print(error_message)
        return {'error': error_message}
async def get_wordpress_categories():
    # Your WordPress website URL
    wordpress_url = get_wordpress_url()
    # REST API endpoint for retrieving categories
    categories_endpoint = wordpress_url + '/wp-json/wp/v2/categories'
    # Send the GET request
    async with httpx.AsyncClient() as client:
        response = await client.get(categories_endpoint)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        return response.json()
    else:
        error_message = f'Failed to retrieve categories. Status code: {response.status_code}'
        print(error_message)
        return {'error': error_message}

async def create_draft_post(post_data):
    # Your WordPress website URL
    wordpress_url = get_wordpress_url()
    # REST API endpoint for creating a draft post
    posts_endpoint = wordpress_url + '/wp-json/wp/v2/posts'
    # Prepare the authentication headers
    username, password = get_wordpress_credentials()
    token = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': f'Basic {token}'
    }
    # Send the POST request with the post data and headers
    async with httpx.AsyncClient() as client:
        response = await client.post(posts_endpoint, headers=headers, json=post_data)
    # Check if the request was successful
    if response.status_code == 201:
        # Parse the JSON response
        response_json = response.json()
        # Return the URL of the created draft post
        return response_json['link']
    else:
        error_message = f'Failed to create draft post. Status code: {response.status_code}'
        print(error_message)
        print(f'Response: {response.text}')  # Debugging information
        print(f'Headers: {headers}')  # Debugging information
        return {'error': error_message}

async def get_draft_posts():
    wordpress_url = get_wordpress_url()
    posts_endpoint = wordpress_url + '/wp-json/wp/v2/posts?status=draft'
    async with httpx.AsyncClient() as client:
        response = await client.get(posts_endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        error_message = f'Failed to retrieve draft posts. Status code: {response.status_code}'
        print(error_message)
        return {'error': error_message}

async def delete_draft_post(post_id):
    wordpress_url = get_wordpress_url()
    delete_endpoint = wordpress_url + f'/wp-json/wp/v2/posts/{post_id}'
    username, password = get_wordpress_credentials()
    token = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': f'Basic {token}'
    }
    async with httpx.AsyncClient() as client:
        response = await client.delete(delete_endpoint, headers=headers)
    if response.status_code == 200:
        return {'success': f'Draft post {post_id} deleted successfully.'}
    else:
        error_message = f'Failed to delete draft post. Status code: {response.status_code}'
        print(error_message)
        return {'error': error_message}
