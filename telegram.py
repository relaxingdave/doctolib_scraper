import os
import logging

from datetime import datetime
import requests

from request_helpers import get_dict_from_url

logging.basicConfig(
    level=logging.INFO
)
logger = logging.getLogger()

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_RECEIVER_ID = os.environ['TELEGRAM_RECEIVER_ID']

# telegram bot receives message with
# url for doctor appointment, latest appointment
# the latest appointment is also when the job expires or when there is an appointment found

class telegram_bot():

    def __init__(self):
        # the jobs have the same id as the telegram update id
        # {update_id: [url, sender_id, end_date]}
        self.jobs_dict = {}
        # To keep track of which update ids were processed
        self.processed_update_ids = set()

    def get_new_doctolib_jobs(self):
        # TODO enable message processing of
        # delete job, add job
        # option to get chat updates of the bot
        telegram_chats = get_dict_from_url(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates",
        )
        new_messages = len(telegram_chats['result'])
        logger.info(f"{new_messages} new messages received in the last 24 hours.")
        # loop over all new chats
        for c in telegram_chats['result']:
            # TODO remove text which is obsolete
            text, url, end_date, sender_id, update_id = self._parse_request_info(c)
            # if the request already is in the dict, skip to next request
            if update_id in self.processed_update_ids:
                logger.info(f"job {update_id} was already processed and is skipped.")
                continue
            self.processed_update_ids.add(update_id)
            # if the request is not in the right format, skip to next request
            if url is None or url.find('start_date=') < 0:
                # send message to sender that format is not correct
                self._send_request_status_message(sender_id, text, successful=False)
                continue
            self.jobs_dict[update_id] = [url, sender_id, end_date]
            logger.info(f"New url {url} added to current jobs dict.")
            self._send_request_status_message(
                telegram_receiver_id=sender_id,
                message=text,
                successful=True
            )

        return self


    def send_availability_message(self, url, receiver_id, next_free_date, end_date):
        """
        Sends a message to the provided Telegram chat id about
        the next available appointment
        """

        message_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

        params = {
            "chat_id": receiver_id,
            "text":f"An appointment on {url} is available on {next_free_date}. Your job will be deleted. If you wish to proceed, send a new message."
        }
        message = requests.post(message_url, params=params)
        if not message.status_code == 200:
            raise RuntimeError("Telegram message could not be sent.")


    def filter_out_inactive_jobs(self):
        for k, v in list(self.jobs_dict.items()):
            if v[2] < datetime.today().date():
                self._send_deleted_job_message(
                    url=v[0],
                    receiver_id=v[1],
                    end_date=v[2].strftime('%Y-%m-%d'),
                )
                del self.jobs_dict[k]

    
    def delete_job(self, job):
        del self.jobs_dict[job]
        self._send_deleted_job_message


    def _send_deleted_job_message(self, url, receiver_id, end_date):
        """
        Sends a message to the provided Telegram chat id about
        the next available appointment
        """

        message_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

        params = {
            "chat_id": receiver_id,
            "text":f"Your request for an appointment at {url} until {end_date} has been deleted because it is outdated."
        }
        message = requests.post(message_url, params=params)
        if not message.status_code == 200:
            raise RuntimeError("Telegram message could not be sent.")


    def _send_request_status_message(self, telegram_receiver_id, message, successful):
        """
        Sends a message to the provided Telegram chat id that
        the requested doctolib job was successful or not.
        success is a boolean.
        """

        message_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

        if successful:
            text = (
                f"Your request '{message}' was accepted. I will let you know when an "
                "appointment available."
            )
        else:
            text = (
                f"Your request '{message}' is not in the right format to start a new request. "
                "Required format: <your json doctolib link>, <last desired date for appointment "
                "in the format DD.MM.YYYY>."
            )

        params = {
            "chat_id": telegram_receiver_id,
            "text": text,
        }
        message = requests.post(message_url, params=params)
        if not message.status_code == 200:
            raise RuntimeError("Telegram message could not be sent.")


    def _parse_request_info(self, message_object):
        """
        Extracts doctolib search request info from message object
        """

        text = message_object['message']['text']
        url = text.split(',')[0].replace(" ", "")
        # we will scrape for 15 days
        url = url.replace('limit=5', 'limit=15')
        sender_id = message_object['message']['from']['id']
        update_id = message_object['update_id']

        # in case date is not in the right format;
        try:
            end_date = text.split(',')[1].replace(" ", "")
            end_date = datetime.strptime(end_date, "%d.%m.%Y").date()
            return text, url, end_date, sender_id, update_id
        except:
            return text, None, None, sender_id, update_id


if __name__ == "__main__":
    telegram_bot = telegram_bot()
    telegram_bot.get_new_doctolib_jobs()
