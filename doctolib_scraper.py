from datetime import datetime, timedelta
import time
import logging

from config import loop_time
from telegram import telegram_bot
from request_helpers import get_dict_from_url

logging.basicConfig(
    level=logging.INFO
)
logger = logging.getLogger()

def main():

    telegram = telegram_bot()

    while True:

        # check if there is an active job
        telegram.get_new_doctolib_jobs()

        # filter out inactive jobs
        telegram.filter_out_inactive_jobs()

        # if there is at least one active job, search for an appointment
        if telegram.jobs_dict:
            logger.info(f"{len(telegram.jobs_dict)} jobs are processed...")

            for j in telegram.jobs_dict.copy():
                url = telegram.jobs_dict[j][0]
                end_date = telegram.jobs_dict[j][2]
                receiver_id = telegram.jobs_dict[j][1]
                next_free_date = get_next_practice_appointment(url, end_date)

                if next_free_date is not None and next_free_date <= end_date:
                    telegram.send_availability_message(
                        url,
                        receiver_id,
                        next_free_date,
                        end_date,
                    )
                    telegram.delete_job(j)

        logger.info(f"Waiting for 60 seconds to update jobs and available appointments...")
        time.sleep(loop_time * 60)


def get_next_practice_appointment(url, end_date):
    """
    Returns the next available slot for an appointment at a provided doctolib
    practice in the period until `end_date`.

    Sometimes the json does not contain a next slot key, so we have to loop over all possible dates.
    """

    search_date = datetime.today().date()
    sd_index = url.find('start_date=') + len('start_date=')

    free_date = None

    # loop over search days every 15 days until the defined `end_date` is reached
    # the json object can only contain max 15 days in advance
    while search_date < end_date:
        search_date_url = (
            url[:sd_index] + search_date.strftime('%Y-%m-%d') + url[sd_index + 10:]
        )
        output_dict = get_dict_from_url(search_date_url)
        # loop over all 15 dates and check if it is available
        for d in output_dict['availabilities']:
            if len(d['slots']) > 0:
                free_date = d['date']
                return datetime.strptime(free_date, '%Y-%m-%d').date()
        search_date += timedelta(days=15)

    # if no date could be found, return None
    return None


if __name__ == "__main__":
    main()
