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
from telegram import send_availability_message

# for logging extract practice id
pos_1 = url.find('practice_ids=')
pos_2 = url[pos_1:].find('&') + pos_1
practice_id_string = url[pos_1:pos_2]

logging.basicConfig(
    filename=f"log_history_{practice_id_string}.log",
    level=logging.INFO
)
logger = logging.getLogger()


def get_next_practice_appointment(url):
    """
    Returns the next available slot for an appointment at a provided doctolib
    doctor.
    """
    output_dict = (
        requests
        .get(url,headers={'User-Agent': 'Mozilla/5.0'})
        .json()
    )
    next_free_date = output_dict['next_slot'][:10]
    next_free_date = datetime.strptime(next_free_date, '%Y-%m-%d').date()
    
    return next_free_date


def main():

    # max date as datetime.date
    max_date = datetime.strptime(latest_date, '%Y-%m-%d').date()

    while True:
        next_free_date = get_next_practice_appointment(url)
        # log results in file
        logger.info(f"{time.strftime('%Y-%m-%d %H:%M:%S')}: {next_free_date}")

        if next_free_date <= max_date:
            os.system("Say An appointment is available.")
            send_availability_message(next_free_date)
            logger.info(f"Date is earlier than {max_date}. Message has been sent out")
            break

        time.sleep(loop_time * 60)


if __name__ == "__main__":
    main()
