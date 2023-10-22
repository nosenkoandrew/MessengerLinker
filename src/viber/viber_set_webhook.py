"""
This file is responsible for setting up a webhook for Viber integration.
A webhook is a URL where Viber can send data to your application.
"""

import json
import requests

with open('../../config.json', 'r') as config_file:
    config_data = json.load(config_file)

# Extract the API credentials
url = "https://chatapi.viber.com/pa/set_webhook"
webhook_url = config_data['viber_webhook_url']  # Replace with your URL
auth_token = config_data['viber_auth_token']  # Replace with your authentication token


def send_post_request():
    data = {
        "url": webhook_url,
        "auth_token": auth_token
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Webhook set successfully.")
    else:
        print("Failed to set the webhook.")

    print(response)
    print(response.text)

send_post_request()
