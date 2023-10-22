import json
from telegram_scrapper import scrape_telegram_channel
from src.utils import create_data_folder

# Load the config data from the file
with open('../config.json', 'r') as config_file:
    config_data = json.load(config_file)

# Extract the API credentials
api_id = config_data['telegram_api_id']
api_hash = config_data['telegram_api_hash']

# Create 'data' folder path
data_folder_path = create_data_folder()

chats = ['asian_ukraine']

for chat in chats:
    chat_data = scrape_telegram_channel(api_id, api_hash, chat)


print("Scraping and data saving completed.")
