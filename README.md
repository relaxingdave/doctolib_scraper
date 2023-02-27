
# TODO
- potentially add parser
- potentially add direct link to the doctor

# doctolib

The script queries a doctolib practice for the next available appointment and sends a telegram message
if an appointment is free before a defined date.

- Run from terminal `pip install -r requirements.txt`
- Create a Telegram bot (write a message to Botfather, define a name, send at least 1 message to the bot)
- Run telegram.py to get the chat_id of the receiver you want to notify
- Create a local .env file with the token from your Telegram bot and the receiver id
- Go to a doctolib doctor's website to book an appointment
- Inspect website - network - reload website - copy get url which gets the availabilities json
- copy this url to the config.py url
- define other settings in config.py
- Run from terminal `dotenv python3 doctolib_scraper.py`
