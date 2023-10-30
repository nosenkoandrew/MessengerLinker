import requests
import json


with open('../config.json', 'r') as config_file:
    config_data = json.load(config_file)

# Extract the API credentials
url = "https://chatapi.viber.com/pa/post"
webhook_url = config_data['viber_webhook_url']  # Replace with your URL
auth_token = config_data['viber_auth_token']  # Replace with your authentication token
user_id = config_data['viber_user_id']  # Replace with your user id


def send_viber_post(post_text, media_url=None):
    """
    Function is currently able to send all posts that has "text-only" or "single-media + text"
    """

    # if we have a media file(s) in post, we need to send an appropriate data parameters
    if media_url:
        data = {
            "auth_token": auth_token,
            "from": user_id,
            "type": "picture",
            "text": post_text,
            "media": media_url,
            "thumbnail": media_url
        }
    # if we don't have a media file(s) in a post, then type of message is text and we send appropriate data parameters
    else:
        data = {
            "auth_token": auth_token,
            "from": user_id,
            "type": "text",
            "text": post_text
        }
    response = requests.post(url, json=data)
