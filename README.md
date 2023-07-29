# doctolib_scraper

The script queries a doctolib practice for the next available appointment and sends a telegram message if an appointment is free before a defined date.

- Run from terminal `pip install -r requirements.txt`
- Create a Telegram bot (write a message to Botfather, define a name, send at least 1 message to the bot)
- Run telegram.py to get the chat_id of the receiver you want to notify
- Create a local .env file with `TELEGRAM_TOKEN` from your Telegram bot and `TELEGRAM_RECEIVER_ID`
- Run from terminal `dotenv python3 doctolib_scraper.py`

If you want to use it:
- Go to a doctolib doctor's website to book an appointment
    - inspect website
    - go to network
    - reload website
    - copy get url which gets the availabilities json
- Send this url to the created bot in the format `<url>, <latest desired date (format DD.MM.YYYY)>`

# TODO
- add direct link to the doctor's website and use selenium to get the json url

