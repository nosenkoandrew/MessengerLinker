import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.viber_messenger import send_viber_post

with open('../config.json', 'r') as config_file:
    config_data = json.load(config_file)

telegram_bot_token = config_data['telegram_bot_token']  # Replace with your telegram bot token
telegram_group_id = config_data['telegram_group_id']  # Replace with your telegram group id

bot = Bot(telegram_bot_token)
dp = Dispatcher(bot)


@dp.channel_post_handler(content_types=types.ContentType.ANY)
async def handle_channel_post(message: types.Message):
    ikb = InlineKeyboardMarkup(row_width=2)
    ikb1 = InlineKeyboardButton(text='Repost to Viber', callback_data='viber')
    ikb2 = InlineKeyboardButton(text='Repost to Whatsapp', callback_data='whatsapp')
    ikb3 = InlineKeyboardButton(text='Skip', callback_data='skip')
    ikb.add(ikb1, ikb2, ikb3)

    content_type = message.content_type
    post_text = message.text if message.text else ''
    media_caption = message.caption if content_type in [types.ContentType.PHOTO, types.ContentType.VIDEO,
                                                        types.ContentType.DOCUMENT] else None

    if content_type == types.ContentType.PHOTO:
        # Handle photos
        media = message.photo[-1].file_id

        # Send both the photo and text in a single message
        full_message = f'{post_text}\n{media_caption}' if media_caption else post_text

        # Send to your group
        await bot.send_photo(telegram_group_id, media, caption=full_message, reply_markup=ikb)

    elif content_type in [types.ContentType.VIDEO, types.ContentType.DOCUMENT]:
        # Handle videos and documents
        media = message.document.file_id

        # Send both the media and text in a single message
        full_message = f'{post_text}\n{media_caption}' if media_caption else post_text

        # Send to your group
        await bot.send_document(telegram_group_id, media, caption=full_message, reply_markup=ikb)

    else:
        # For text posts or unsupported content types, send the post text with inline buttons
        await bot.send_message(telegram_group_id, post_text, reply_markup=ikb)


@dp.callback_query_handler(lambda c: c.data in ['viber', 'whatsapp', 'skip'])
async def repost_callback(callback: types.CallbackQuery):
    if callback.data == "viber":
        await callback.answer(text='Reposting to Viber')

        # post_text = callback.message.reply_to_message.text
        post_text = callback.message.text
        send_viber_post(post_text)

        # Remove the "Reposting to Viber" button after clicking on it
        ikb = callback.message.reply_markup
        ikb.inline_keyboard = [[button for button in row if button.text != 'Repost to Viber'] for row in
                               ikb.inline_keyboard]

        # Edit the message to hide the button
        await callback.message.edit_reply_markup(reply_markup=ikb)
    elif callback.data == 'whatsapp':
        await callback.answer(text='Reposting to Whatsapp')
        print("Reposting to Whatsapp!")

        # Remove the "Reposting to Viber" button after clicking on it
        ikb = callback.message.reply_markup
        ikb.inline_keyboard = [[button for button in row if button.text != 'Repost to Whatsapp'] for row in
                               ikb.inline_keyboard]

        # Edit the message to hide the button
        await callback.message.edit_reply_markup(reply_markup=ikb)

    else:
        await callback.answer(text='Post will not be reposted')
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
