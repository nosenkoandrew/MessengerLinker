import json
import datetime
import os
from telethon.sync import TelegramClient
from telethon.tl.types import DocumentAttributeVideo, DocumentAttributeAnimated
from utils import create_media_directory, create_data_folder, construct_file_path


def scrape_telegram_channel(api_id, api_hash, chat):
    """
    Function to scrape the posts from a telegram channel
    """
    data_list = []

    # Create a directory to store media files
    media_directory = create_media_directory()

    with TelegramClient('TelegramScraperClient', api_id, api_hash) as client:
        for message in client.iter_messages(chat, offset_date=datetime.date.today(), reverse=True):
            media_file = None
            if message.media:
                if hasattr(message.media, 'document') and any(
                        isinstance(attribute, DocumentAttributeVideo) for attribute in
                        message.media.document.attributes):
                    # Handle video
                    video_file = os.path.join(media_directory, f'video_{message.id}.mp4')
                    client.download_media(message, video_file)
                elif hasattr(message.media, 'document'):
                    # Handle GIF
                    if any(isinstance(attribute, DocumentAttributeAnimated) for attribute in
                           message.media.document.attributes):
                        gif_file = os.path.join(media_directory, f'gif_{message.id}.gif')
                        client.download_media(message, gif_file)
                    else:
                        # Handle other documents (non-GIFs)
                        other_doc_file = os.path.join(media_directory, f'other_doc_{message.id}')
                        client.download_media(message, other_doc_file)
                elif hasattr(message.media, 'photo'):
                    # Handle photo
                    media_file = os.path.join(media_directory, f'media_{message.id}.jpg')
                    client.download_media(message, media_file)

            data = {
                'group': chat,
                'sender': message.sender_id,
                'text': message.text,
                'date': message.date.strftime('%Y-%m-%d %H:%M:%S'),
                'media_url': media_file
            }
            data_list.append(data)

    data_folder = create_data_folder()

    # Construct the full file path for the JSON file
    json_file_path = construct_file_path(data_folder, "data_{}.json".format(datetime.date.today()))

    # Save the data list to a JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(data_list, json_file)

    return data_list
