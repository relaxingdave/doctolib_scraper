import os

import requests

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_RECEIVER_ID = os.environ['TELEGRAM_RECEIVER_ID']

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


def send_availability_message(next_free_date):
    """
    Sends a message to the provided Telegram chat id about
    the next available appointment
    """

    message_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    params = {
        "chat_id": TELEGRAM_RECEIVER_ID,
        "text":f"An appointment is available on {next_free_date}."
    }
    message = requests.post(message_url, params=params)
    if not message.status_code == 200:
        raise RuntimeError("Telegram message could not be sent.")

if __name__ == "__main__":
    get_telegram_chat_id()
