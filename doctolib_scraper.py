# copy to new folder, new project
# create requirements txt with required data in that folder
# pip install and test
# upload to git

import os
from datetime import datetime
import time
import logging

import requests

from config import latest_date, url, loop_time

logging.basicConfig(filename="log_history.log", level=logging.INFO)
logger = logging.getLogger()

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_RECEIVER_ID = os.environ['TELEGRAM_RECEIVER_ID']

message_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

def main():

    max_date = datetime.strptime(latest_date, '%Y-%m-%d').date()

    while True:
        output_dict = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).json()
        next_free_date = output_dict['next_slot'][:10]
        next_free_date = datetime.strptime(next_free_date, '%Y-%m-%d').date()
        # log results in file
        logger.info(f"{time.strftime('%Y-%m-%d %H:%M:%S')}: {next_free_date}")

        if next_free_date < max_date:
            os.system("Say An appointment is available.")
            params = {
                "chat_id": TELEGRAM_RECEIVER_ID,
                "text":f"An appointment is available on {next_free_date}."
            }
            message = requests.post(message_url, params=params)
            if not message.status_code == 200:
                raise RuntimeError("Telegram message could not be sent.")
            break

        time.sleep(loop_time * 60)


if __name__ == "__main__":
    main()
