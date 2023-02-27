import os

import requests

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

def get_telegram_chat_id():
    # get the chats of my bot (first we have to send a message to the bot)
    telegram_chats = (
        requests
        .get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates")
        .json()
    )
    # find my chat id by selecting the from_id of the first message
    to_id = telegram_chats['result'][0]['message']['from']

    print(f"Your telegram chat id is {to_id}.")

if __name__ == "__main__":
    get_telegram_chat_id()
