import requests
import json


with open('../../config.json', 'r') as config_file:
    config_data = json.load(config_file)

# Extract the API credentials
url = "https://chatapi.viber.com/pa/post"
webhook_url = config_data['viber_webhook_url']  # Replace with your URL
auth_token = config_data['viber_auth_token']  # Replace with your authentication token
user_id = config_data['viber_user_id']  # Replace with your user id


def send_viber_post(post_text, media_url=None):
    """
    Function is currently able to send all "text-only" posts
    """

    data = {
        "auth_token": auth_token,
        "from": user_id,
        "type": "text",
        "text": post_text
    }
    response = requests.post(url, json=data)

    print(response)
    print(response.text)


with open('../../data/data_2023-10-20.json', 'r') as file:
    telegram_posts = json.load(file)

for telegram_post in telegram_posts:
    viber_post_text = telegram_post.get('text', '')
    send_viber_post(viber_post_text)
