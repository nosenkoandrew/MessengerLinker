"""
You may use this file in case you need to get your group_id
"""

import json
from aiogram import Bot, Dispatcher, executor, types


with open('../../config.json', 'r') as config_file:
    config_data = json.load(config_file)

telegram_bot_token = config_data['telegram_bot_token']
bot = Bot(telegram_bot_token)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    print("id:", message.chat.id)
    await bot.send_message(chat_id=message.chat.id,
                           text='hello')

if __name__ == "__main__":
    executor.start_polling(dp)