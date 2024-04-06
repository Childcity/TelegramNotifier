#! /usr/bin/env python3

from ast import Await
import asyncio
import json
from telegram import Bot
from telegram.error import TelegramError
import time

def read_config():
    with open('src/TeleggaHelperBot.json', 'r') as file:
        return json.load(file)

async def edit_channel_messages(bot: Bot, chat_id):
    try:
         async with bot:
            #await bot.send_message(chat_id=chat_id, text='USP-Python has started up!')

            # chat = bot.get_chat(chat_id)
            print(await bot.get_me())
            updates = (await bot.get_updates())[0]
            print(updates)
            
            messages = await bot.get_chat_history(chat_id=chat_id, limit=100)  # You can adjust the limit as needed

            for message in messages:
                # Check if the message is editable (not pinned, not service message)
                if message.text and not message.pinned and not message.service:
                    # Edit the message
                    # bot.edit_message_text(chat_id=CHANNEL_ID, message_id=message.message_id, text="Your updated message here")

                    # Introduce a delay to avoid flooding the Telegram API
                    time.sleep(1)  # Adjust as necessary

    except TelegramError as e:
        print("An error occurred:", e)
    
async def main():
    config = read_config()
    bot = Bot(token=config['token'])
    await edit_channel_messages(bot, config['chat_id'])


if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())